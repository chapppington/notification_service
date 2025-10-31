from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from logic.commands.base import (
    BaseCommand,
    BaseCommandHandler,
    CommandResultType,
    CommandType,
)
from logic.exceptions.mediator import CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    commands_map: dict[CommandType, BaseCommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_command(
        self,
        command: CommandType,
        command_handlers: Iterable[BaseCommandHandler[CommandType, CommandResultType]],
    ):
        self.commands_map[command].extend(command_handlers)

    async def handle_command(
        self,
        command: BaseCommand,
    ) -> Iterable[CommandResultType]:
        command_type = command.__class__

        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]
