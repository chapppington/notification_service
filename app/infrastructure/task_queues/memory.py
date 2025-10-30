from dataclasses import dataclass

from infrastructure.task_queues.base import BaseTaskQueue


@dataclass
class DummyInMemoryTaskQueue(BaseTaskQueue):
    async def send_task(self, task_name: str, *args, **kwargs):
        return type("Result", (), {"id": f"memory-{task_name}"})()

    def send_task_sync(self, task_name: str, *args, **kwargs):
        return type("Result", (), {"id": f"memory-{task_name}"})()

    async def get_task_result(self, task_id: str):
        return {"id": task_id, "status": "SUCCESS"}
