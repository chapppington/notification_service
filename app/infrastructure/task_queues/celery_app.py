from celery import Celery

from settings.config import Config


config = Config()

celery_app = Celery(
    "notification_service",
    broker=config.redis_connection_uri,
    backend=config.redis_connection_uri,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    result_expires=3600,
)

# Import tasks to register them with Celery
from infrastructure.task_queues import celery_tasks  # noqa: E402, F401
