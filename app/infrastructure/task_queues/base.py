from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseTaskQueue(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def send_task(self, task_name: str, *args, **kwargs) -> Any: ...

    @abstractmethod
    def send_task_sync(self, task_name: str, *args, **kwargs) -> Any: ...

    @abstractmethod
    async def get_task_result(self, task_id: str) -> Any: ...

    @abstractmethod
    def register_task(self, task_name: str, task_func: callable): ...
