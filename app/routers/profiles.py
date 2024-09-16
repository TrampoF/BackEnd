from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request

from app.application.register_profile import Input as RegisterProfileInput, RegisterProfile
from app.database.database_connection import PostgresAdapter
from app.database.supabase_adapter import SupabaseAdapter
from app.repository.profile_repository_database import ProfileRepositoryDatabase
from app.repository.profile_repository_supabase import ProfileRepositorySupabase


router = APIRouter(
    prefix="/profiles",
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
async def register_user(
    request: Annotated[RegisterProfileInput, Form()],
    profile_repository: ProfileRepositorySupabase = Depends(),
):
    """
    Register a profile.
    """
    res = RegisterProfile(profile_repository=profile_repository).execute(request)
    return res
