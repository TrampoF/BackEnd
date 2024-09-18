from abc import ABC, abstractmethod
from uuid import UUID

from app.models.profile import Profile
from app.schemas.register_profile_schema import RegisterProfileSchema


class IProfileRepository(ABC):
    """
    Interface for profile repository.
    """

    @abstractmethod
    def get_profiles(self):
        """
        Retrieve all profiles.
        """

    @abstractmethod
    def get_profile_by_id(self, profile_id: UUID) -> Profile | None:
        """
        Retrieve an profiles by id
        """

    @abstractmethod
    def register(self, profile_data: RegisterProfileSchema) -> Profile:
        """
        Register a new user and creates a profile.
        """

    @abstractmethod
    def get_profile_by_email(self, email: str) -> Profile | None:
        """
        Retrieve a profile by email.
        """
