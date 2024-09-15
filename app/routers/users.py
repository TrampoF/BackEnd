from fastapi import APIRouter, Depends

from app.repository.user_repository import UserRepository


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.get("/register")
async def register_user(user_repository: UserRepository = Depends()):
    """
    Register a user.
    """
    return {"message": user_repository}
