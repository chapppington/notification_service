from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.user.base import BaseUserRepository
from infrastructure.repositories.user.mongo import MongoDBUsersRepository
from infrastructure.task_queues.base import BaseTaskQueue
from infrastructure.task_queues.celery_adapter import CeleryTaskQueue
from infrastructure.task_queues.celery_app import celery_app
from logic.mediator import Mediator
from logic.services.notification import (
    BaseNotificationService,
    ComposedNotificationService,
)
from logic.services.user import (
    BaseUserService,
    MongoUserService,
)
from logic.use_cases.user import (
    CreateUserUseCase,
    CreateUserUseCaseHandler,
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

    container.register(
        BaseUserService,
        MongoUserService,
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
        BaseNotificationService,
        ComposedNotificationService,
        scope=Scope.singleton,
    )

    container.register(CreateUserUseCaseHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_use_case(
            use_case=CreateUserUseCase,
            use_case_handlers=[
                container.resolve(CreateUserUseCaseHandler),
            ],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
