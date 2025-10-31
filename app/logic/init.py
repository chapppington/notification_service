from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from domain.user.interfaces.base_repository import BaseUserRepository
from domain.user.service import UserService
from infrastructure.database.repositories.user.mongo import MongoDBUsersRepository
from infrastructure.task_queues.base import BaseTaskQueue
from infrastructure.task_queues.celery_adapter import CeleryTaskQueue
from infrastructure.task_queues.celery_app import celery_app
from logic.commands.user import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from logic.mediator import Mediator
from logic.services.notification import (
    BaseNotificationService,
    ComposedNotificationService,
)
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_user_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )
        return MongoDBUsersRepository(
            mongo_db_client=client,
            mongo_db_database_name=config.mongodb_user_database,
            mongo_db_collection_name=config.mongodb_user_collection,
        )

    container.register(
        BaseUserRepository,
        factory=init_user_mongodb_repository,
        scope=Scope.singleton,
    )

    def init_task_queue():
        return CeleryTaskQueue(celery_app=celery_app)

    container.register(
        BaseTaskQueue,
        factory=init_task_queue,
        scope=Scope.singleton,
    )

    container.register(
        UserService,
        scope=Scope.singleton,
    )

    container.register(
        BaseNotificationService,
        ComposedNotificationService,
        scope=Scope.singleton,
    )

    container.register(CreateUserCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            command=CreateUserCommand,
            command_handlers=[
                container.resolve(CreateUserCommandHandler),
            ],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
