"""
This module defines the channels router.
"""

from fastapi import APIRouter


router = APIRouter(
    prefix="/channels",
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_channels():
    """
    Retrieve all channels.
    """
    raise NotImplementedError
