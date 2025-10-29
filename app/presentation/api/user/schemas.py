from pydantic import BaseModel

from domain.entities.user import UserEntity


class CreateUserRequestSchema(BaseModel):
    username: str
    email: str
    telegram: str
    phone: str


class CreateUserResponseSchema(BaseModel):
    oid: str
    username: str
    email: str
    telegram: str
    phone: str

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "CreateUserResponseSchema":
        return cls(
            oid=entity.oid,
            username=entity.username.as_generic_type(),
            email=entity.email.as_generic_type(),
            telegram=entity.telegram.as_generic_type(),
            phone=entity.phone.as_generic_type(),
        )
