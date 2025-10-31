from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.user.value_objects import (
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
