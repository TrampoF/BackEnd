import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.repository.i_channel_repository import IChannelRepository
from app.repository.i_tag_repository import ITagRepository


class Input(BaseModel):
    model_config = ConfigDict(extra="ignore")
    channel_name: str
    profile_id: uuid.UUID
    chat_identifier: str = Field(..., min_length=1)
    tags: list[str]


class RegisterChannel:

    _channel_repository: IChannelRepository
    _tag_repository: ITagRepository

    def __init__(
        self, channel_repository: IChannelRepository, tag_repository: ITagRepository
    ):
        self._channel_repository = channel_repository
        self._tag_repository = tag_repository

    def execute(self, channel_data: Input) -> uuid.UUID:
        channel_data = Input.model_validate(channel_data)
        created_channel = self._channel_repository.create_channel(channel_data)
        return created_channel.id
