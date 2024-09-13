"""
This module defines the IUserRepository interface.
"""

from abc import ABC, abstractmethod


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
    def get_by_id(self, user_id):
        """
        Retrieve a user by their ID.
        """
