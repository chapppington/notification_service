from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from domain.entities.user import UserEntity
from infrastructure.task_queues.base import BaseTaskQueue


@dataclass
class BaseNotificationService(ABC):
    @abstractmethod
    async def send(self, subject: str, message: str, user: UserEntity) -> str: ...


@dataclass
class EmailNotificationService(BaseNotificationService):
    task_queue: BaseTaskQueue

    async def send(self, subject: str, message: str, user: UserEntity) -> str:
        result = await self.task_queue.send_task(
            "send_email_notification",
            email=user.email.as_generic_type(),
            username=user.username.as_generic_type(),
            subject=subject,
            message=message,
        )
        return result.id if hasattr(result, "id") else str(result)


@dataclass
class TelegramNotificationService(BaseNotificationService):
    task_queue: BaseTaskQueue

    async def send(self, subject: str, message: str, user: UserEntity) -> str:
        result = await self.task_queue.send_task(
            "send_telegram_notification",
            telegram=user.telegram.as_generic_type(),
            username=user.username.as_generic_type(),
            subject=subject,
            message=message,
        )
        return result.id if hasattr(result, "id") else str(result)


@dataclass
class SmsNotificationService(BaseNotificationService):
    task_queue: BaseTaskQueue

    async def send(self, subject: str, message: str, user: UserEntity) -> str:
        result = await self.task_queue.send_task(
            "send_sms_notification",
            phone=user.phone.as_generic_type(),
            username=user.username.as_generic_type(),
            subject=subject,
            message=message,
        )
        return result.id if hasattr(result, "id") else str(result)


@dataclass
class ComposedNotificationService(BaseNotificationService):
    notification_services: Iterable[BaseNotificationService]

    async def send(self, subject: str, message: str, user: UserEntity) -> str:
        """Tries services one by one until one succeeds.

        Returns task_id of the first successful service.

        """
        last_error = None

        for service in self.notification_services:
            try:
                task_id = await service.send(subject, message, user)
                return task_id
            except Exception as e:
                last_error = e
                continue

        raise Exception(
            f"All notification services failed. Last error: {str(last_error)}",
        )
