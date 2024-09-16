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

    def get_all(self) -> list[Profile]:
        profiles = self._session.query(Profile).all()
        return profiles

    def get_by_id(self, profile_id) -> None | Profile:
        profile = self._session.query(Profile).filter(Profile.id == profile_id).first()
        return profile

    def create_profile(self, profile: dict) -> None:
        self._session.add(Profile(**profile))
