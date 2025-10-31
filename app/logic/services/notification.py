from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.user.entities import UserEntity
from infrastructure.task_queues.base import BaseTaskQueue


@dataclass
class BaseNotificationService(ABC):
    @abstractmethod
    async def send(self, subject: str, message: str, user: UserEntity) -> str: ...


@dataclass
class ComposedNotificationService(BaseNotificationService):
    task_queue: BaseTaskQueue

    async def send(self, subject: str, message: str, user: UserEntity) -> str:
        """Send notification with fallback (Email -> Telegram -> SMS) in
        Worker."""
        result = await self.task_queue.send_task(
            "send_notification_with_fallback",
            email=user.email.as_generic_type(),
            telegram=user.telegram.as_generic_type(),
            phone=user.phone.as_generic_type(),
            username=user.username.as_generic_type(),
            subject=subject,
            message=message,
        )
        return result.id if hasattr(result, "id") else str(result)
