import re
from dataclasses import dataclass

from domain.exceptions.user import (
    EmptyEmailException,
    EmptyPhoneException,
    EmptyTelegramException,
    EmptyUsernameException,
    InvalidEmailException,
    InvalidPhoneException,
    InvalidTelegramException,
    UsernameTooLongException,
)
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class UsernameValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyUsernameException()

        if len(self.value) > 50:
            raise UsernameTooLongException(text=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class EmailValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyEmailException()

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, self.value):
            raise InvalidEmailException(email=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


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


@dataclass(frozen=True)
class PhoneValueObject(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyPhoneException()

        # Remove common formatting characters (spaces, dashes, parentheses, plus)
        digits_only = re.sub(r"[^\d]", "", self.value)

        # Phone number validation rules:
        # - Must contain only digits (after removing formatting)
        # - Length between 10 and 15 digits (international standard)
        # - Can start with + in the original value
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise InvalidPhoneException(phone=self.value)

        # Check if original value contains only valid phone characters
        # Allow: digits, +, spaces, dashes, parentheses
        phone_pattern = r"^[\+]?[\d\s\-\(\)]{10,}$"
        if not re.match(phone_pattern, self.value):
            raise InvalidPhoneException(phone=self.value)

        # Ensure it contains at least some digits
        if not digits_only:
            raise InvalidPhoneException(phone=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
