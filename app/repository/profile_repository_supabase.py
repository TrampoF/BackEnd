from uuid import UUID

from supabase import Client
from app.models.profile import Profile
from app.repository.i_profile_repository import IProfileRepository


class ProfileRepositorySupabase(IProfileRepository):
    """
    ProfileRepositorySupabase implements the IProfileRepository
    interface for profile-related supabase operations.
    """

    def __init__(
        self,
        client: Client,
    ) -> None:
        self._client = client

    def get_all(self):
        pass

    def get_by_id(self, profile_id: UUID) -> Profile | None:
        profile = (
            self._client.table(Profile.__tablename__)
            .select("*")
            .eq(Profile.id.name, profile_id)
            .execute()
        )
        if len(profile.data) == 0:
            return None
        return Profile(**profile.data[0])

    def register(self, profile: dict) -> Profile:
        profile = self._client.auth.sign_up(
            {
                "email": profile["email"],
                "password": profile["password"],
                "options": {
                    "data": {
                        "first_name": profile["first_name"],
                        "last_name": profile["last_name"],
                    }
                },
            }
        )
        return Profile(
            id=profile.user.id,
            first_name=profile.user.user_metadata["first_name"],
            last_name=profile.user.user_metadata["last_name"],
            email=profile.user.email,
            created_at=profile.user.created_at,
            updated_at=profile.user.updated_at,
        )

    def get_by_email(self, email: str) -> Profile | None:
        profile = (
            self._client.table(Profile.__tablename__)
            .select("*")
            .eq(Profile.email.name, email)
            .execute()
        )
        if len(profile.data) == 0:
            return None
        return Profile(**profile.data[0])
