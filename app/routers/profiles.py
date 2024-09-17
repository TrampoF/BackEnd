from fastapi import APIRouter, Depends, Request, Response
from supabase import Client

from app.application.register_profile import (
    RegisterProfile,
)
from app.database.supabase_adapter import SupabaseAdapter
from app.repository.profile_repository_supabase import ProfileRepositorySupabase


router = APIRouter(
    prefix="/profiles",
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=200)
async def register_user(
    request: Request,
    response: Response,
    client: Client = Depends(SupabaseAdapter().get_db),
):
    """
    Register a profile.
    """
    try:
        async with request.form() as form:
            profile = RegisterProfile(
                profile_repository=ProfileRepositorySupabase(client=client)
            ).execute(dict(form))
        return profile
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}
