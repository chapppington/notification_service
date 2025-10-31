import pytest
from faker import Faker

from domain.user.entities import UserEntity
from domain.user.exceptions import UserAlreadyExistsException
from domain.user.interfaces.base_repository import BaseUserRepository
from domain.user.value_objects import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)
from logic.commands.user import CreateUserCommand
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_user_command_success(
    user_repository: BaseUserRepository,
    mediator: Mediator,
    faker: Faker,
):
    username = faker.user_name()[:50]
    email = faker.email()
    telegram = "@" + faker.user_name()
    phone = "+1 (555) 123-4567"

    user: UserEntity
    user, *_ = await mediator.handle_command(
        CreateUserCommand(
            username=username,
            email=email,
            telegram=telegram,
            phone=phone,
        ),
    )

    assert await user_repository.check_user_exists_by_username(
        username=user.username.as_generic_type(),
    )


@pytest.mark.asyncio
async def test_create_user_command_username_already_exists(
    user_repository: BaseUserRepository,
    mediator: Mediator,
    faker: Faker,
):
    username = faker.user_name()[:50]
    existing_user = UserEntity.create_user(
        username=UsernameValueObject(value=username),
        email=EmailValueObject(value=faker.email()),
        telegram=TelegramValueObject(value="@" + faker.user_name()),
        phone=PhoneValueObject(value="+1 (555) 123-4567"),
    )
    # Simulate saved user
    await user_repository.add_user(existing_user)

    with pytest.raises(UserAlreadyExistsException):
        await mediator.handle_command(
            CreateUserCommand(
                username=username,
                email=faker.email(),
                telegram="@" + faker.user_name(),
                phone="+1 (555) 123-4567",
            ),
        )
