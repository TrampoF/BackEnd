"""
This module contains test cases for the profile registration functionality.
"""

from pydantic_core import ValidationError
import pytest
from app.application.get_profile import GetProfile
from app.application.register_profile import RegisterProfile
from app.database.database_connection import PostgresAdapter
from app.database.supabase_adapter import SupabaseAdapter
from app.exceptions.invalid_email_format_exception import InvalidEmailFormatException
from app.exceptions.password_confirmation_dot_not_match_exception import (
    PasswordConfirmationDotNotMatchException,
)
from app.repository.profile_repository_database import ProfileRepositoryDatabase
from app.repository.profile_repository_memory import ProfileRepositoryMemory
from app.repository.profile_repository_supabase import ProfileRepositorySupabase

profile_repository: ProfileRepositorySupabase = ProfileRepositorySupabase(
    client=SupabaseAdapter().get_db()
)

# profile_repository: ProfileRepositoryMemory = ProfileRepositoryMemory()


class TestRegisterProfile:
    """
    Test suite for profile registration functionality.
    """

    def test_should_register_profile(self):
        """
        Test that profile should be registered
        """
        profile_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": "foo@bar.com",
            "password": "password",
            "password_confirmation": "password",
        }
        registered_profile_id = RegisterProfile(
            profile_repository=profile_repository
        ).execute(data=profile_data)
        registered_profile = GetProfile(profile_repository=profile_repository).execute(
            profile_id=registered_profile_id
        )
        assert registered_profile_id == registered_profile.id
        assert profile_data["first_name"] == registered_profile.first_name
        assert profile_data["last_name"] == registered_profile.last_name
        assert profile_data["email"] == registered_profile.email
        assert (
            f'{profile_data["first_name"]} {profile_data["last_name"]}'
            == registered_profile.full_name
        )

    def test_should_not_register_profile_with_different_password_and_password_confirmation(
        self,
    ):
        """
        Test that profile should not be registered if password and password confimation is different
        """
        profile_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": "foo@bar.com",
            "password": "password",
            "password_confirmation": "password1232",
        }
        with pytest.raises(PasswordConfirmationDotNotMatchException) as excinfo:
            RegisterProfile(profile_repository=profile_repository).execute(
                data=profile_data
            )
        assert str(excinfo.value) == "Password and password confirmation do not match!"

    def test_should_not_register_profile_with_wrong_email_format(self):
        """
        Test that profile should not be registered if email do not match the corrrect format
        """
        profile_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": "foobar.com",
            "password": "password",
            "password_confirmation": "password",
        }
        with pytest.raises(InvalidEmailFormatException) as excinfo:
            RegisterProfile(profile_repository=profile_repository).execute(
                data=profile_data
            )
        assert str(excinfo.value) == "Invalid email format"

    profile_empty_field_data = [
        (
            {
                "first_name": "",
                "last_name": "Bar",
                "email": "foo@bar.com",
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
                "password": "",
                "password_confirmation": "password",
            },
            "String should have at least 8 characters",
        ),
    ]

    @pytest.mark.parametrize("test_input, expected", profile_empty_field_data)
    def test_should_not_register_profile_with_empty_field(self, test_input, expected):
        """
        Test that profile should not be registered if any required data is empty
        """

        with pytest.raises(ValidationError) as excinfo:
            RegisterProfile(profile_repository=profile_repository).execute(
                data=test_input
            )
        assert str(excinfo.value.errors()[0]["msg"]) == expected

    profile_missing_field_data = [
        (
            {
                "last_name": "Bar",
                "email": "foo@bar.com",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "email": "foo@bar.com",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "password_confirmation": "password",
            }
        ),
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "password": "password",
            }
        ),
    ]

    @pytest.mark.parametrize("test_input", profile_missing_field_data)
    def test_should_not_register_profile_with_missing_field(self, test_input):
        """
        Test that profile should not be registered if any required data is missing
        """

        with pytest.raises(ValidationError) as excinfo:
            RegisterProfile(profile_repository=profile_repository).execute(
                data=test_input
            )
        assert str(excinfo.value.errors()[0]["msg"]) == "Field required"

    def test_should_not_register_profile_with_an_profilename_or_email_already_registered(
        self,
    ):
        """
        Test that profile should not be registered if profilename or email is already registered
        """

        assert False
