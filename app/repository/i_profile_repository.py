from abc import ABC, abstractmethod
from uuid import UUID


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
    def create_profile(self, profile: dict):
        """
        Insert profile into profiles table
        """

    @abstractmethod
    def get_by_id(self, profile_id: UUID):
        """
        Retrieve an [rpfile] by id
        """

    @abstractmethod
    def register(self, profile: dict):
        """
        Register a new user
        """
