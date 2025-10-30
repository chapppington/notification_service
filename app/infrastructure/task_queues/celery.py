from dataclasses import dataclass
from typing import Any

from celery import Celery
from celery.result import AsyncResult

from infrastructure.task_queues.base import BaseTaskQueue


@dataclass
class CeleryTaskQueue(BaseTaskQueue):
    broker_url: str
    backend_url: str
    app_name: str = "notification_service"
    _celery_app: Celery | None = None

    def __post_init__(self):
        self._celery_app = Celery(
            self.app_name,
            broker=self.broker_url,
            backend=self.backend_url,
        )

        self._celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
            task_track_started=True,
            task_time_limit=30 * 60,  # 30 minutes
            task_soft_time_limit=25 * 60,  # 25 minutes
            result_expires=3600,  # 1 hour
        )

    async def start(self):
        pass

    async def close(self):
        if self._celery_app:
            self._celery_app.control.shutdown()

    async def send_task(self, task_name: str, *args, **kwargs) -> Any:
        result = self._celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return result

    def send_task_sync(self, task_name: str, *args, **kwargs) -> Any:
        result = self._celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return result

    async def get_task_result(self, task_id: str) -> Any:
        result = AsyncResult(task_id, app=self._celery_app)
        if result.ready():
            return result.get()
        return None

    def register_task(self, task_name: str, task_func: callable):
        self._celery_app.task(name=task_name)(task_func)

    @property
    def celery_app(self) -> Celery:
        return self._celery_app
