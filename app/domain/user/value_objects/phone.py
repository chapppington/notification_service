import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.user.exceptions import (
    EmptyPhoneException,
    InvalidPhoneException,
)


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
