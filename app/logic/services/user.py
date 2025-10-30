from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.user import UserEntity
from domain.value_objects.user import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)
from infrastructure.repositories.user.base import BaseUserRepository
from logic.exceptions.user import UserAlreadyExistsException


@dataclass
class BaseUserService(ABC):
    @abstractmethod
    async def create_user(
        self,
        username: str,
        email: str,
        telegram: str,
        phone: str,
    ) -> UserEntity: ...


@dataclass
class MongoUserService(BaseUserService):
    user_repository: BaseUserRepository

    async def create_user(
        self,
        username: str,
        email: str,
        telegram: str,
        phone: str,
    ) -> UserEntity:
        if await self.user_repository.check_user_exists_by_username(username):
            raise UserAlreadyExistsException(username=username)

        username_vo = UsernameValueObject(value=username)
        email_vo = EmailValueObject(value=email)
        telegram_vo = TelegramValueObject(value=telegram)
        phone_vo = PhoneValueObject(value=phone)

        new_user = UserEntity.create_user(
            username=username_vo,
            email=email_vo,
            telegram=telegram_vo,
            phone=phone_vo,
        )

        await self.user_repository.add_user(new_user)

        return new_user
