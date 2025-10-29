from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)


@dataclass(frozen=True)
class BaseUseCase(ABC): ...


UseCaseType = TypeVar("UseCaseType", bound=BaseUseCase)
UseCaseResultType = TypeVar("UseCaseResultType", bound=Any)


@dataclass(frozen=True)
class BaseUseCaseHandler(ABC, Generic[UseCaseType, UseCaseResultType]):
    @abstractmethod
    async def handle(self, use_case: UseCaseType) -> UseCaseResultType: ...
