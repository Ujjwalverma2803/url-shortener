from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas import ClickEvent
from tasks import track_click
from database import get_db
from models import Click

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/track")
async def track(payload: ClickEvent):
    track_click.delay(
        slug=payload.slug,
        ip=payload.ip,
        user_agent=payload.user_agent,
        referrer=payload.referrer
    )
    return {"status": "queued"}

@router.get("/stats/{slug}")
def get_stats(
    slug: str,
    db: Session = Depends(get_db)
):
    total = db.query(
        func.count(Click.id)
    ).filter(
        Click.slug == slug
    ).scalar()

    by_device = db.query(
        Click.device_type,
        func.count(Click.id)
    ).filter(
        Click.slug == slug
    ).group_by(
        Click.device_type
    ).all()

    by_browser = db.query(
        Click.browser,
        func.count(Click.id)
    ).filter(
        Click.slug == slug
    ).group_by(
        Click.browser
    ).all()

    return {
        "slug": slug,
        "total_clicks": total,
        "by_device": {
            d: c for d, c in by_device
        },
        "by_browser": {
            b: c for b, c in by_browser
        }
    }

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "analytics"
    }