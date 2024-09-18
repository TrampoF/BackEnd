import os
import random
from pydantic_core import ValidationError
import pytest
from supabase import create_client
from app.application.get_profile import GetProfile
from app.application.register_profile import RegisterProfile
from app.exceptions.invalid_email_format_exception import InvalidEmailFormatException
from app.exceptions.password_confirmation_dot_not_match_exception import (
    PasswordConfirmationDotNotMatchException,
)
from app.exceptions.email_already_taken_exception import EmailAlreadyTakenException
from app.repository.profile_repository_memory import ProfileRepositoryMemory
from app.repository.profile_repository_supabase import ProfileRepositorySupabase


@pytest.fixture()
def db():
    """
    Fixture for Supabase database connection.
    """
    client = create_client(
        os.getenv("SUPABASE_URL", "http://localhost:5432"),
        os.getenv("SUPABASE_KEY", "postgres"),
    )
    return client


@pytest.fixture()
def profile_repository(db):
    """
    Fixture for profile repository.
    """
    return ProfileRepositoryMemory()


class TestRegisterProfile:
    """
    Test suite for profile registration functionality.
    """

    def test_should_register_profile(self, profile_repository):
        """
        Test that profile should be registered
        """

        profile_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": f"foo{random.random()}@bar.com",
            "password": "password",
            "password_confirmation": "password",
        }
        registered_profile_id = RegisterProfile(
            profile_repository=profile_repository
        ).execute(profile_data)
        registered_profile = GetProfile(profile_repository=profile_repository).execute(
            profile_id=registered_profile_id
        )
        print(registered_profile)
        assert registered_profile_id == registered_profile.id
        assert profile_data["first_name"] == registered_profile.first_name
        assert profile_data["last_name"] == registered_profile.last_name
        assert profile_data["email"] == registered_profile.email
        assert (
            f'{profile_data["first_name"]} {profile_data["last_name"]}'
            == registered_profile.full_name
        )

    def test_should_not_register_profile_with_different_password_and_password_confirmation(
        self, profile_repository
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

    def test_should_not_register_profile_with_wrong_email_format(
        self, profile_repository
    ):
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
    def test_should_not_register_profile_with_empty_field(
        self, test_input, expected, profile_repository
    ):
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
    def test_should_not_register_profile_with_missing_field(
        self, test_input, profile_repository
    ):
        """
        Test that profile should not be registered if any required data is missing
        """

        with pytest.raises(ValidationError) as excinfo:
            RegisterProfile(profile_repository=profile_repository).execute(
                data=test_input
            )
        assert str(excinfo.value.errors()[0]["msg"]) == "Field required"

    profile_duplicated_email_data = [
        (
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "password": "password",
                "password_confirmation": "password",
            },
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "foo@bar.com",
                "password": "password",
                "password_confirmation": "password",
            },
            "This email is already taken",
        )
    ]

    @pytest.mark.parametrize(
        "user1_data, user2_data, expected", profile_duplicated_email_data
    )
    def test_should_not_register_profile_with_an_email_already_registered(
        self, user1_data, user2_data, expected, profile_repository
    ):
        """
        Test that profile should not be registered if email is already registered
        """

        with pytest.raises(EmailAlreadyTakenException) as excinfo:
            RegisterProfile(profile_repository=profile_repository).execute(
                data=user1_data
            )
            RegisterProfile(profile_repository=profile_repository).execute(
                data=user2_data
            )
        assert str(excinfo.value) == expected
