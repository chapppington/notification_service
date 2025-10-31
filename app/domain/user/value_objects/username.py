from dataclasses import dataclass

from domain.base.value_object import BaseValueObject
from domain.user.exceptions import (
    EmptyUsernameException,
    UsernameTooLongException,
)


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
