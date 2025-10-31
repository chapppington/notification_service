from dataclasses import dataclass

from domain.user.entities import UserEntity
from domain.user.interfaces.base_repository import BaseUserRepository
from infrastructure.database.converters.user import (
    convert_user_document_to_entity,
    convert_user_entity_to_document,
)
from infrastructure.database.repositories.base.mongo import BaseMongoDBRepository


@dataclass
class MongoDBUsersRepository(BaseUserRepository, BaseMongoDBRepository):
    async def get_user_by_oid(self, oid: str) -> UserEntity | None:
        user_document = await self._collection.find_one(filter={"oid": oid})

        if not user_document:
            return None

        return convert_user_document_to_entity(user_document)

    async def check_user_exists_by_username(self, username: str) -> bool:
        return bool(await self._collection.find_one(filter={"username": username}))

    async def add_user(self, user: UserEntity) -> None:
        await self._collection.insert_one(convert_user_entity_to_document(user))
