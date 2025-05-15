__all__ = [
    "celery_app"
]

from notify_service.celery import app as celery_app