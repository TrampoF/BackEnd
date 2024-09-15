from uuid import UUID
from app.repository.iuser_repository import IUserRepository


class UserRepositoryMemory(IUserRepository):
    """
    UserRepositoryMemory implements the IUserepository
    interface for user-related memory operations.
    """

    _users = list[dict]

    def __init__(self):
        self._users = []

    def get_all(self) -> list[dict]:
        return self._users

    def create_user(self, user: dict) -> None:
        self._users.append(user)

    def get_by_id(self, user_id: UUID) -> None | dict:
        return next((item for item in self._users if item["id"] == user_id), None)
