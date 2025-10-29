from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.user import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)


@dataclass(eq=False)
class UserEntity(BaseEntity):
    username: UsernameValueObject
    email: EmailValueObject
    telegram: TelegramValueObject
    phone: PhoneValueObject

    @classmethod
    def create_user(
        cls,
        username: UsernameValueObject,
        email: EmailValueObject,
        telegram: TelegramValueObject,
        phone: PhoneValueObject,
    ) -> "UserEntity":
        new_user = cls(
            username=username,
            email=email,
            telegram=telegram,
            phone=phone,
        )
        return new_user
