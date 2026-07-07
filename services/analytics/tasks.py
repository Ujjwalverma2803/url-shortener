from celery import Celery
from config import settings
from database import SessionLocal
from models import Click
from utils.geo import parse_user_agent

celery_app = Celery(
    "analytics",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(
    name="track_click",
    max_retries=3,
    default_retry_delay=5
)
def track_click(
    slug: str,
    ip: str,
    user_agent: str,
    referrer: str
):
    db = SessionLocal()
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
    except Exception as exc:
        db.rollback()
        raise track_click.retry(exc=exc)
    finally:
        db.close()