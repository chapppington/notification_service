from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UserException(ApplicationException):
    @property
    def message(self) -> str:
        return "Chat exception occurred"


@dataclass(eq=False)
class UsernameTooLongException(UserException):
    text: str

    @property
    def message(self) -> str:
        return f"Username too long: {self.text[:30]}..."


@dataclass(eq=False)
class EmptyUsernameException(UserException):
    @property
    def message(self) -> str:
        return "Username is empty"


@dataclass(eq=False)
class EmptyEmailException(UserException):
    @property
    def message(self) -> str:
        return "Email is empty"


@dataclass(eq=False)
class EmptyTelegramException(UserException):
    @property
    def message(self) -> str:
        return "Telegram username is empty"


@dataclass(eq=False)
class EmptyPhoneException(UserException):
    @property
    def message(self) -> str:
        return "Phone number is empty"


@dataclass(eq=False)
class InvalidEmailException(UserException):
    email: str

    @property
    def message(self) -> str:
        return f"Invalid email format: {self.email}"


@dataclass(eq=False)
class InvalidTelegramException(UserException):
    telegram: str

    @property
    def message(self) -> str:
        return f"Invalid telegram username format: {self.telegram}"


@dataclass(eq=False)
class InvalidPhoneException(UserException):
    phone: str

    @property
    def message(self) -> str:
        return f"Invalid phone number format: {self.phone}"
