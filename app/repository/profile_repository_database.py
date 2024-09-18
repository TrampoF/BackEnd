from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.repository.i_profile_repository import IProfileRepository


class ProfileRepositoryDatabase(IProfileRepository):
    """
    ProfileRepositoryDatabase implements the IProfileRepository
    interface for profile-related database operations.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_profiles(self) -> list[Profile]:
        profiles = self._session.query(Profile).all()
        return profiles

    def get_profile_by_id(self, profile_id) -> None | Profile:
        profile = self._session.query(Profile).filter(Profile.id == profile_id).first()
        return profile

    def register(self, profile_data) -> Profile:
        profile = Profile(**profile_data.model_dump())
        self._session.add(profile)
        return profile

    def get_profile_by_email(self, email) -> None | Profile:
        profile = self._session.query(Profile).filter(Profile.email == email).first()
        return profile
