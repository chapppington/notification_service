from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UseCaseHandlersNotRegisteredException(LogicException):
    use_case_type: type

    @property
    def message(self) -> str:
        return f"Use case handlers not registered for use case type: {self.use_case_type.__name__}"
