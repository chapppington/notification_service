from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.user import UserEntity


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def check_user_exists_by_username(self, username: str) -> bool: ...

    @abstractmethod
    async def add_user(self, user: UserEntity): ...

    @abstractmethod
    async def get_user_by_oid(self, oid: str) -> UserEntity | None: ...
