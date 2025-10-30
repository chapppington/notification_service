from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    mongodb_connection_uri: str = Field(alias="MONGO_DB_CONNECTION_URI")
    mongodb_user_database: str = Field(default="user", alias="MONGODB_USER_DATABASE")
    mongodb_user_collection: str = Field(
        default="user",
        alias="MONGODB_USER_COLLECTION",
    )

    redis_connection_uri: str = Field(
        default="redis://redis:6379/0",
        alias="REDIS_CONNECTION_URI",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
