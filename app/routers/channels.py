from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, Response
from sqlalchemy.orm import Session

from app.application.register_channel import Input as RegisterChannelInput
from app.application.register_channel import RegisterChannel
from app.database.database_connection import PostgresAdapter
from app.queue.rabbitmq_adapter import RabbitMQAdapter
from app.repository.channel_repository_database import ChannelRepositoryDatabase
from app.repository.tag_repository_database import TagRepositoryDatabase


router = APIRouter(
    prefix="/channels",
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=200)
async def register_channel(
    request_body: Annotated[RegisterChannelInput, Form()],
    response: Response,
    session: Session = Depends(PostgresAdapter().get_db),
    queue=Depends(RabbitMQAdapter),
):
    """
    Retrieve all channels.
    """
    try:
        channel = RegisterChannel(
            channel_repository=ChannelRepositoryDatabase(session=session),
            tag_repository=TagRepositoryDatabase(session=session),
            queue=queue,
        ).execute(request_body)
        return {"message": "Channel registered successfully", "data": channel}
    except Exception as e:
        response.status_code = 400
        return {"error": str(e)}
