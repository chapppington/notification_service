from typing import (
    Any,
    Mapping,
)

from domain.entities.user import UserEntity
from domain.value_objects.user import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)


def convert_user_entity_to_document(user: UserEntity) -> dict:
    return {
        "oid": user.oid,
        "username": user.username.as_generic_type(),
        "email": user.email.as_generic_type(),
        "telegram": user.telegram.as_generic_type(),
        "phone": user.phone.as_generic_type(),
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


def convert_user_document_to_entity(user_document: Mapping[str, Any]) -> UserEntity:
    return UserEntity(
        oid=user_document["oid"],
        username=UsernameValueObject(value=user_document["username"]),
        email=EmailValueObject(value=user_document["email"]),
        telegram=TelegramValueObject(value=user_document["telegram"]),
        phone=PhoneValueObject(value=user_document["phone"]),
        created_at=user_document["created_at"],
        updated_at=user_document["updated_at"],
    )
