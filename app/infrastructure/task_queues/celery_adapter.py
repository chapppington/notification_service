from dataclasses import dataclass
from typing import Any

from celery import Celery
from celery.result import AsyncResult

from infrastructure.task_queues.base import BaseTaskQueue


@dataclass
class CeleryTaskQueue(BaseTaskQueue):
    celery_app: Celery

    async def send_task(self, task_name: str, *args, **kwargs) -> Any:
        result = self.celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return result

    def send_task_sync(self, task_name: str, *args, **kwargs) -> Any:
        result = self.celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return result

    async def get_task_result(self, task_id: str) -> Any:
        result = AsyncResult(task_id, app=self.celery_app)
        if result.ready():
            return result.get()
        return None
