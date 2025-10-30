import pytest

from domain.exceptions.user import (
    EmptyEmailException,
    EmptyPhoneException,
    EmptyTelegramException,
    EmptyUsernameException,
    InvalidEmailException,
    InvalidPhoneException,
    InvalidTelegramException,
    UsernameTooLongException,
)
from domain.value_objects.user import (
    EmailValueObject,
    PhoneValueObject,
    TelegramValueObject,
    UsernameValueObject,
)


@pytest.mark.parametrize(
    "username,should_raise",
    [
        ("john_doe", False),
        ("", True),
        ("a" * 51, True),
    ],
)
def test_username_value_object(username, should_raise):
    if should_raise:
        with pytest.raises((EmptyUsernameException, UsernameTooLongException)):
            UsernameValueObject(value=username)
    else:
        obj = UsernameValueObject(value=username)
        assert obj.as_generic_type() == username


@pytest.mark.parametrize(
    "email,should_raise",
    [
        ("user@example.com", False),
        ("", True),
        ("invalid-email", True),
        ("no-domain@", True),
        ("@no-local.com", True),
    ],
)
def test_email_value_object(email, should_raise):
    if should_raise:
        with pytest.raises((EmptyEmailException, InvalidEmailException)):
            EmailValueObject(value=email)
    else:
        obj = EmailValueObject(value=email)
        assert obj.as_generic_type() == email


@pytest.mark.parametrize(
    "telegram,should_raise",
    [
        ("@telegram", False),
        ("telegram_user", False),
        ("", True),
        ("ab", True),
        ("1startwithdigit", True),
        ("has-dash", True),
    ],
)
def test_telegram_value_object(telegram, should_raise):
    if should_raise:
        with pytest.raises((EmptyTelegramException, InvalidTelegramException)):
            TelegramValueObject(value=telegram)
    else:
        obj = TelegramValueObject(value=telegram)
        assert obj.as_generic_type() == telegram


@pytest.mark.parametrize(
    "phone,should_raise",
    [
        ("+1 (555) 123-4567", False),
        ("5551234567", False),
        ("", True),
        ("123", True),
        ("++1234567890", True),
        ("invalid-phone", True),
    ],
)
def test_phone_value_object(phone, should_raise):
    if should_raise:
        with pytest.raises((EmptyPhoneException, InvalidPhoneException)):
            PhoneValueObject(value=phone)
    else:
        obj = PhoneValueObject(value=phone)
        assert obj.as_generic_type() == phone
