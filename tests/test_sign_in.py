import os
import random
import pytest
from supabase import create_client

from app.application.register_profile import RegisterProfile
from app.application.sign_in import SignIn
from app.repository.profile_repository_supabase import ProfileRepositorySupabase
from app.services.auth_service_supabase import AuthServiceSupabase


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
def auth_service(db):
    """
    Fixture for profile repository.
    """
    return AuthServiceSupabase(client=db)


class TestSignIn:
    def test_should_sign_in_registered_user(self, auth_service):
        profile_data = f"foo{random.random()}@bar.com"
        profile_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": f"{profile_data}",
            "password": "password",
            "password_confirmation": "password",
        }
        RegisterProfile(profile_repository=ProfileRepositorySupabase(db)).execute(
            profile_data
        )
        response = SignIn(auth_service=auth_service).execute(profile_data)
        assert profile_data["email"] == response["email"]
