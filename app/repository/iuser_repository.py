from abc import ABC, abstractmethod
from uuid import UUID


class IUserRepository(ABC):
    """
    Interface for user repository.
    """

    @abstractmethod
    def get_all(self):
        """
        Retrieve all users.
        """

    @abstractmethod
    def create_user(self, user: dict):
        """
        Insert user into users table
        """

    @abstractmethod
    def get_by_id(self, user_id: UUID):
        """
        Retrieve an user by id
        """
