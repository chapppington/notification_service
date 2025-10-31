from dataclasses import dataclass

from domain.user.entities import UserEntity
from domain.user.service import UserService
from logic.commands.base import (
    BaseCommand,
    BaseCommandHandler,
)
from logic.services.notification import BaseNotificationService


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    email: str
    telegram: str
    phone: str


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler[CreateUserCommand, UserEntity]):
    user_service: UserService
    notification_service: BaseNotificationService

    async def handle(self, command: CreateUserCommand) -> UserEntity:
        user = await self.user_service.create_user(
            username=command.username,
            email=command.email,
            telegram=command.telegram,
            phone=command.phone,
        )

        await self.notification_service.send(
            subject="Welcome to Notification Service!",
            message=f"Hello {user.username.as_generic_type()}! Your account has been created successfully.",
            user=user,
        )

        return user
