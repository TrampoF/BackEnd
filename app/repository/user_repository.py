from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database_connection import PostgresAdapter
from app.models.user import User
from app.repository.iuser_repository import IUserRepository


class UserRepository(IUserRepository):
    """
    UserRepository implements the IUserRepository interface for user-related database operations.
    """

    def __init__(self, session: Session = Depends(PostgresAdapter().get_db)):
        self._session = session

    def get_all(self):
        channels = self._session.query(User).all()
        return channels

    def get_by_id(self, user_id):
        user = self._session.query(User).filter(User.id == user_id).first()
        return user
