from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from logic.exceptions.mediator import UseCaseHandlersNotRegisteredException
from logic.use_cases.base import (
    BaseUseCase,
    BaseUseCaseHandler,
    UseCaseResultType,
    UseCaseType,
)


@dataclass(eq=False)
class Mediator:
    use_cases_map: dict[UseCaseType, BaseUseCaseHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_use_case(
        self,
        use_case: UseCaseType,
        use_case_handlers: Iterable[BaseUseCaseHandler[UseCaseType, UseCaseResultType]],
    ):
        self.use_cases_map[use_case].extend(use_case_handlers)

    async def handle_use_case(
        self,
        use_case: BaseUseCase,
    ) -> Iterable[UseCaseResultType]:
        use_case_type = use_case.__class__

        handlers = self.use_cases_map.get(use_case_type)

        if not handlers:
            raise UseCaseHandlersNotRegisteredException(use_case_type)

        return [await handler.handle(use_case) for handler in handlers]
