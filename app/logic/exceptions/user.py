from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserAlreadyExistsException(LogicException):
    username: str

    @property
    def message(self) -> str:
        return f"User with username '{self.username}' already exists"


@dataclass(eq=False)
class UserNotFoundException(LogicException):
    user_oid: str

    @property
    def message(self) -> str:
        return f"User with oid '{self.user_oid}' not found"
