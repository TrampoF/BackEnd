import datetime
from typing import List
import uuid
from app.models.profile import Profile
from app.repository.i_profile_repository import IProfileRepository
from app.schemas.register_profile_schema import RegisterProfileSchema


class ProfileRepositoryMemory(IProfileRepository):
    """
    ProfileRepositoryMemory implements the IProfileRepository
    interface for profile-related memory operations.
    """

    _profiles = List[Profile]

    def __init__(self):
        self._profiles = []

    def get_profiles(self) -> List[Profile]:
        return self._profiles

    def register(self, profile_data: RegisterProfileSchema) -> Profile:
        profile_data = RegisterProfileSchema(
            **profile_data.model_dump(),
        )
        profile = Profile(
            id=uuid.uuid4(),
            email=profile_data.email,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        self._profiles.append(profile)
        return profile

    def get_profile_by_id(self, profile_id: uuid.UUID) -> Profile | None:
        return next((item for item in self._profiles if item.id == profile_id), None)

    def get_profile_by_email(self, email: str) -> Profile | None:
        return next((item for item in self._profiles if item.email == email), None)
