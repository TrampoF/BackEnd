from uuid import UUID
from typing import List

from supabase import Client
from app.models.profile import Profile
from app.repository.i_profile_repository import IProfileRepository
from app.schemas.register_profile_schema import RegisterProfileSchema


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

    def get_profiles(self) -> List[Profile]:
        return self._client.table(Profile.__tablename__).select("*").execute()

    def get_profile_by_id(self, profile_id: UUID) -> Profile | None:
        profile = (
            self._client.table(Profile.__tablename__)
            .select("*")
            .eq(Profile.id.name, profile_id)
            .execute()
        )
        if len(profile.data) == 0:
            return None
        return Profile(**profile.data[0])

    def register(self, profile_data: RegisterProfileSchema) -> Profile:
        registered_profile = self._client.auth.sign_up(
            {
                "email": profile_data.email,
                "password": profile_data.password,
                "options": {
                    "data": {
                        "first_name": profile_data.first_name,
                        "last_name": profile_data.last_name,
                    }
                },
            }
        )
        return Profile(
            id=registered_profile.user.id,
            first_name=registered_profile.user.user_metadata["first_name"],
            last_name=registered_profile.user.user_metadata["last_name"],
            email=registered_profile.user.email,
            created_at=registered_profile.user.created_at,
            updated_at=registered_profile.user.updated_at,
        )

    def get_profile_by_email(self, email: str) -> Profile | None:
        profile = (
            self._client.table(Profile.__tablename__)
            .select("*")
            .eq(Profile.email.name, email)
            .execute()
        )
        if len(profile.data) == 0:
            return None
        return Profile(**profile.data[0])
