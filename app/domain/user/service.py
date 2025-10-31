from dataclasses import dataclass

from domain.user.entities import UserEntity
from domain.user.exceptions import UserAlreadyExistsException
from domain.user.interfaces.base_repository import BaseUserRepository
from domain.user.value_objects import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)


@dataclass
class UserService:
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
