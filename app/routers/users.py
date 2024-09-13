"""
This module defines the users router.
"""

from fastapi import APIRouter, Depends

from app.application.GetAllUsers import GetAllUsers
from app.repository.UserRepository import UserRepository


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users(user_repository: UserRepository = Depends()):
    """
    Retrieve a list of users from the repository.
    """
    users = GetAllUsers(user_repository=user_repository).run()
    return users
