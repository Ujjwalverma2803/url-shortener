from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas import ClickEvent
from database import get_db
from models import Click
from utils.geo import parse_user_agent

router = APIRouter(prefix="/analytics", tags=["analytics"])

def save_click(
    slug: str,
    ip: str,
    user_agent: str,
    referrer: str
):
    db = next(get_db())
    try:
        device_info = parse_user_agent(user_agent)
        click = Click(
            slug=slug,
            ip_address=ip,
            device_type=device_info["device_type"],
            browser=device_info["browser"],
            referrer=referrer or None
        )
        db.add(click)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

@router.post("/track")
async def track(
    payload: ClickEvent,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        save_click,
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