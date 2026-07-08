from fastapi import (
    APIRouter, Depends,
    HTTPException, Request,
    status, Security
)
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from schemas import URLCreate, URLResponse
from models import URL
from utils.base62 import generate_short_slug
from utils.cache import (
    get_cached_url,
    cache_url,
    invalidate_cache,
    check_rate_limit
)
from database import get_db
from dependencies import get_current_user
from config import settings
import httpx

router = APIRouter(tags=["urls"])
security = HTTPBearer()

@router.post(
    "/shorten",
    response_model=URLResponse,
    status_code=status.HTTP_201_CREATED
)
async def shorten_url(
    payload: URLCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user_id = current_user["sub"]
    tier = current_user["tier"]

    if not check_rate_limit(user_id, tier):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily URL limit reached for your plan"
        )

    if payload.custom_slug:
        if tier != "premium":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Custom slugs are a premium feature"
            )
        existing = db.query(URL).filter(
            URL.short_slug == payload.custom_slug
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Custom slug already taken"
            )
        slug = payload.custom_slug
        is_custom = True
    else:
        slug = generate_short_slug()
        while db.query(URL).filter(
            URL.short_slug == slug
        ).first():
            slug = generate_short_slug()
        is_custom = False

    url = URL(
        original_url=str(payload.original_url),
        short_slug=slug,
        user_id=user_id,
        custom_slug=is_custom,
        expires_at=payload.expires_at
    )
    db.add(url)
    db.commit()
    db.refresh(url)

    cache_url(slug, str(payload.original_url))

    return {
        "id": url.id,
        "original_url": url.original_url,
        "short_slug": url.short_slug,
        "short_url": f"{settings.base_url}/{slug}",
        "click_count": url.click_count,
        "expires_at": url.expires_at,
        "created_at": url.created_at
    }

@router.get("/my-urls")
def get_my_urls(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    urls = db.query(URL).filter(
        and_(
            URL.user_id == current_user["sub"],
            URL.is_active == True
        )
    ).all()
    return urls

@router.get("/{slug}")
async def redirect_url(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    cached = get_cached_url(slug)
    if cached:
        await fire_analytics(slug, request)
        return RedirectResponse(
            url=cached,
            status_code=status.HTTP_302_FOUND
        )

    url = db.query(URL).filter(
        and_(
            URL.short_slug == slug,
            URL.is_active == True
        )
    ).first()

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )

    if url.expires_at and url.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This URL has expired"
        )

    cache_url(slug, url.original_url)
    url.click_count += 1
    db.commit()

    await fire_analytics(slug, request)

    return RedirectResponse(
        url=url.original_url,
        status_code=status.HTTP_302_FOUND
    )

@router.delete("/{slug}")
def delete_url(
    slug: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    url = db.query(URL).filter(
        and_(
            URL.short_slug == slug,
            URL.user_id == current_user["sub"]
        )
    ).first()
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found or unauthorized"
        )
    url.is_active = False
    db.commit()
    invalidate_cache(slug)
    return {"message": "URL deleted successfully"}

async def fire_analytics(slug: str, request: Request):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://url-analytics-k782.onrender.com/analytics/track",
                json={
                    "slug": slug,
                    "ip": request.client.host,
                    "user_agent": request.headers.get(
                        "user-agent", ""
                    ),
                    "referrer": request.headers.get(
                        "referer", ""
                    )
                },
                timeout=5.0
            )
    except Exception:
        pass