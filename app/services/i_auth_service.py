from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, auth_data: dict):
        """
        Sign in a user.
        """
