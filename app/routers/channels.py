"""
This module defines the channels router.
"""

from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form, Request, Response, status
from fastapi.datastructures import FormData

from app.application.RegisterChannel import RegisterChannel, RegisterChannelInput
from app.repository.ChannelRepositoryDatabase import ChannelRepositoryDatabase


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


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_channel(
    response: Response,
    body: Annotated[RegisterChannelInput, Form()],
    channel_respository: ChannelRepositoryDatabase = Depends(),
):
    """
    Create a new channel.
    """
    try:
        registered_channel = RegisterChannel(channel_respository).run(
            register_input=dict(body)
        )
        return registered_channel
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(e)}
