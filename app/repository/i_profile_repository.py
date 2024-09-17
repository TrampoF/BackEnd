from abc import ABC, abstractmethod
from uuid import UUID

from app.models.profile import Profile


class IProfileRepository(ABC):
    """
    Interface for profile repository.
    """

    @abstractmethod
    def get_all(self):
        """
        Retrieve all profiles.
        """

    @abstractmethod
    def get_by_id(self, profile_id: UUID) -> Profile | None:
        """
        Retrieve an profiles by id
        """

    @abstractmethod
    def register(self, profile: dict) -> Profile:
        """
        Register a new user and creates a profile.
        """

    @abstractmethod
    def get_by_email(self, email: str) -> Profile | None:
        """
        Retrieve a profile by email.
        """
