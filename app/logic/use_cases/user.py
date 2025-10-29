from dataclasses import dataclass

from domain.entities.user import UserEntity
from logic.services.user import BaseUserService
from logic.use_cases.base import (
    BaseUseCase,
    BaseUseCaseHandler,
)


@dataclass(frozen=True)
class CreateUserUseCase(BaseUseCase):
    username: str
    email: str
    telegram: str
    phone: str


@dataclass(frozen=True)
class CreateUserUseCaseHandler(BaseUseCaseHandler[CreateUserUseCase, UserEntity]):
    user_service: BaseUserService

    async def handle(self, use_case: CreateUserUseCase) -> UserEntity:
        return await self.user_service.create_user(
            username=use_case.username,
            email=use_case.email,
            telegram=use_case.telegram,
            phone=use_case.phone,
        )
