import re
from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.user.exceptions import (
    EmptyEmailException,
    InvalidEmailException,
)


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
