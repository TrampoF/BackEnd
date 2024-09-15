"""
This module contains test cases for the user registration functionality.
"""

from pydantic_core import ValidationError
import pytest
from app.application.get_user import GetUser
from app.application.register_user import RegisterUser
from app.exceptions.invalid_email_format_exception import InvalidEmailFormatException
from app.exceptions.password_confirmation_dot_not_match_exception import (
    PasswordConfirmationDotNotMatchException,
)
from app.repository.user_repository_memory import UserRepositoryMemory

user_repository: UserRepositoryMemory = UserRepositoryMemory()


class TestRegisterUser:
    """
    Test suite for user registration functionality.
    """

    def test_should_register_user(self):
        """
        Test that user should be registered
        """
        user_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": "foo@bar.com",
            "username": "fooBar",
            "password": "password",
            "password_confirmation": "password",
        }
        registered_user_id = RegisterUser(user_repository=user_repository).execute(
            data=user_data
        )
        registered_user = GetUser(user_repository=user_repository).execute(
            user_id=registered_user_id
        )
        assert registered_user_id == registered_user.id
        assert user_data["first_name"] == registered_user.first_name
        assert user_data["last_name"] == registered_user.last_name
        assert user_data["email"] == registered_user.email
        assert user_data["username"] == registered_user.username
        assert (
            f'{user_data["first_name"]} {user_data["last_name"]}'
            == registered_user.full_name
        )

    def test_should_not_register_user_with_different_password_and_password_confirmation(
        self,
    ):
        """
        Test that user should not be registered if password and password confimation is different
        """
        user_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": "foo@bar.com",
            "username": "fooBar",
            "password": "password",
            "password_confirmation": "password1232",
        }
        with pytest.raises(PasswordConfirmationDotNotMatchException) as excinfo:
            RegisterUser(user_repository=user_repository).execute(data=user_data)
        assert str(excinfo.value) == "Password and password confirmation do not match!"

    def test_should_not_register_user_with_wrong_email_format(self):
        """
        Test that user should not be registered if email do not match the corrrect format
        """
        user_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": "foobar.com",
            "username": "fooBar",
            "password": "password",
            "password_confirmation": "password",
        }
        with pytest.raises(InvalidEmailFormatException) as excinfo:
            RegisterUser(user_repository=user_repository).execute(data=user_data)
        assert str(excinfo.value) == "Invalid email format"

    user_empty_field_data = [
        (
            {
                "first_name": "",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password": "password",
                "password_confirmation": "password",
            },
            "String should have at least 1 character",
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password": "password",
                "password_confirmation": "password",
            },
            "String should have at least 1 character",
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "",
                "username": "fooBar",
                "password": "password",
                "password_confirmation": "password",
            },
            "String should have at least 1 character",
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "username": "",
                "password": "password",
                "password_confirmation": "password",
            },
            "String should have at least 1 character",
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password": "",
                "password_confirmation": "password",
            },
            "String should have at least 8 characters",
        ),
    ]

    @pytest.mark.parametrize("test_input, expected", user_empty_field_data)
    def test_should_not_register_user_with_empty_field(self, test_input, expected):
        """
        Test that user should not be registered if any required data is empty
        """

        with pytest.raises(ValidationError) as excinfo:
            RegisterUser(user_repository=user_repository).execute(data=test_input)
        assert str(excinfo.value.errors()[0]["msg"]) == expected

    user_missing_field_data = [
        (
            {
                "last_name": "Bar",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "username": "fooBar",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "username": "fooBar",
                "password": "password",
            }
        ),
    ]

    @pytest.mark.parametrize("test_input", user_missing_field_data)
    def test_should_not_register_user_with_missing_field(self, test_input):
        """
        Test that user should not be registered if any required data is missing
        """

        with pytest.raises(ValidationError) as excinfo:
            RegisterUser(user_repository=user_repository).execute(data=test_input)
        assert str(excinfo.value.errors()[0]["msg"]) == "Field required"

    def test_should_not_register_user_with_an_username_or_email_already_registered(
        self,
    ):
        """
        Test that user should not be registered if username or email is already registered
        """

        assert False
