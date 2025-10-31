from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f"Use case handlers not registered for use case type: {self.command_type.__name__}"
