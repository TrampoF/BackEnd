from supabase import Client
from app.services.i_auth_service import IAuthService


class AuthServiceSupabase(IAuthService):
    """
    AuthServiceSupabase implements the IAuthService interface for
    authentication-related supabase operations.
    """

    def __init__(
        self,
        client: Client,
    ) -> None:
        self._client = client

    def sign_in(self, auth_data: dict):
        user = self._client.auth.sign_in_with_password(
            {"email": auth_data["email"], "password": auth_data["password"]},
        )
        print(dict(user))
        return {
            "access_token": user.session.access_token,
            "refresh_token": user.session.refresh_token,
            "email": user.user.email,
        }
