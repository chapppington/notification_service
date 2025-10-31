from dataclasses import (
    dataclass,
    field,
)

from domain.user.entities import UserEntity
from domain.user.interfaces.base_repository import BaseUserRepository


@dataclass
class DummyInMemoryUserRepository(BaseUserRepository):
    _saved_users: list[UserEntity] = field(default_factory=list, kw_only=True)

    async def check_user_exists_by_username(self, username: str) -> bool:
        try:
            return (
                next(
                    user
                    for user in self._saved_users
                    if user.username.as_generic_type() == username
                )
                is not None
            )
        except StopIteration:
            return False

    async def add_user(self, user: UserEntity):
        self._saved_users.append(user)

    async def get_user_by_oid(self, oid: str) -> UserEntity | None:
        try:
            return next(user for user in self._saved_users if user.oid == oid)
        except StopIteration:
            return None
