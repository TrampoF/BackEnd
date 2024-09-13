"""
This module defines the interface for database connections.
"""

from abc import ABC, abstractmethod


class IDatabaseConnection(ABC):
    """
    Interface for database connections.
    """

    @abstractmethod
    def get_db(self):
        """
        Retrieve the database connection.
        """
