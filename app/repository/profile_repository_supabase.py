import datetime
from uuid import UUID

from fastapi import Depends
from supabase import Client
from app.database.supabase_adapter import SupabaseAdapter
from app.models.profile import Profile
from app.repository.i_profile_repository import IProfileRepository


class ProfileRepositorySupabase(IProfileRepository):
    """
    ProfileRepositorySupabase implements the IProfileRepository
    interface for profile-related supabase operations.
    """

    def __init__(
        self,
        client: Client = Depends(SupabaseAdapter().get_db),
    ) -> None:
        self._client = client

    def get_all(self):
        pass

    def create_profile(self, profile: dict):
        pass

    def get_by_id(self, profile_id: UUID):
        profile = (
            self._client.table(Profile.__tablename__)
            .select()
            .eq(Profile.id.name, profile_id)
            .execute()
        )
        return profile

    def register(self, profile: dict):
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
        return profile
