import pytest
from faker import Faker

from domain.entities.user import UserEntity
from domain.value_objects.user import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)
from infrastructure.repositories.user.base import BaseUserRepository
from logic.exceptions.user import UserAlreadyExistsException
from logic.mediator import Mediator
from logic.use_cases.user import CreateUserUseCase


@pytest.mark.asyncio
async def test_create_user_use_case_success(
    user_repository: BaseUserRepository,
    mediator: Mediator,
    faker: Faker,
):
    username = faker.user_name()[:50]
    email = faker.email()
    telegram = "@" + faker.user_name()
    phone = "+1 (555) 123-4567"

    user: UserEntity
    user, *_ = await mediator.handle_use_case(
        CreateUserUseCase(
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
async def test_create_user_use_case_username_already_exists(
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
        await mediator.handle_use_case(
            CreateUserUseCase(
                username=username,
                email=faker.email(),
                telegram="@" + faker.user_name(),
                phone="+1 (555) 123-4567",
            ),
        )
