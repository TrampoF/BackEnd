"""
Module to get all users.
"""

import datetime
from typing import List
from pydantic import BaseModel
from app.repository.IUserRepository import IUserRepository


class Output(BaseModel):
    """
    DTO for user output.
    """

    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GetAllUsers:
    """
    Class to handle the retrieval of all users.
    """

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def run(self) -> List[Output] | None:
        users = self._user_repository.get_all()
        if (users is None) or (len(users) == 0):
            return None
        return [Output(**user.__dict__) for user in users]
