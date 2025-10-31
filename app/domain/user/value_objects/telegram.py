import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.user.exceptions import (
    EmptyTelegramException,
    InvalidTelegramException,
)


@dataclass(frozen=True)
class TelegramValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTelegramException()

        # Remove @ if present for validation
        username = self.value.lstrip("@")

        # Telegram username rules:
        # - 5-32 characters
        # - Only letters, numbers, and underscores
        # - Must start with a letter
        if len(username) < 5 or len(username) > 32:
            raise InvalidTelegramException(telegram=self.value)

        telegram_pattern = r"^[a-zA-Z][a-zA-Z0-9_]{4,31}$"

        if not re.match(telegram_pattern, username):
            raise InvalidTelegramException(telegram=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
