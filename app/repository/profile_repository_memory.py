from uuid import UUID
from app.repository.i_profile_repository import IProfileRepository


class ProfileRepositoryMemory(IProfileRepository):
    """
    ProfileRepositoryMemory implements the IProfileRepository
    interface for profile-related memory operations.
    """

    _profiles = list[dict]

    def __init__(self):
        self._profiles = []

    def get_all(self) -> list[dict]:
        return self._profiles

    def create_profile(self, profile: dict) -> None:
        self._profiles.append(profile)

    def get_by_id(self, profile_id: UUID) -> None | dict:
        return next((item for item in self._profiles if item["id"] == profile_id), None)
