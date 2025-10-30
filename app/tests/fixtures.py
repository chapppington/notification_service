from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.user.base import BaseUserRepository
from infrastructure.repositories.user.memory import DummyInMemoryUserRepository
from infrastructure.task_queues.base import BaseTaskQueue
from infrastructure.task_queues.memory import DummyInMemoryTaskQueue
from logic.init import _init_container
from logic.services.notification import (
    BaseNotificationService,
    ComposedNotificationService,
)


def init_dummy_container() -> Container:
    container = _init_container()

    # Use in-memory users repository
    container.register(
        BaseUserRepository,
        DummyInMemoryUserRepository,
        scope=Scope.singleton,
    )

    # Use in-memory task queue for tests
    container.register(BaseTaskQueue, DummyInMemoryTaskQueue, scope=Scope.singleton)

    # Ensure composed notification service uses dummy queue
    container.register(
        BaseNotificationService,
        ComposedNotificationService,
        scope=Scope.singleton,
    )

    return container
