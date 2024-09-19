import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.queue.i_queue import IQueue
from app.repository.i_channel_repository import IChannelRepository
from app.repository.i_tag_repository import ITagRepository


class Input(BaseModel):
    model_config = ConfigDict(extra="ignore")
    channel_name: str
    profile_id: uuid.UUID
    chat_identifier: str = Field(..., min_length=1)
    tags: list[str]
    api_id: str = Field(..., min_length=1)
    api_hash: str = Field(..., min_length=1)


class RegisterChannel:

    _channel_repository: IChannelRepository
    _tag_repository: ITagRepository
    _queue: IQueue

    def __init__(
        self,
        channel_repository: IChannelRepository,
        tag_repository: ITagRepository,
        queue: IQueue,
    ):
        self._channel_repository = channel_repository
        self._tag_repository = tag_repository
        self._queue = queue

    def execute(self, channel_data: Input) -> uuid.UUID:
        channel_data = Input.model_validate(channel_data)
        created_channel = self._channel_repository.create_channel(channel_data)
        self._queue.create_queue("telethon_queue")
        self._queue.publish(
            "",
            "telethon_queue",
            {
                "chat_identifier": created_channel.chat_identifier,
                "api_id": created_channel.api_id,
                "api_hash": created_channel.api_hash,
                "channel_id": str(created_channel.id),
            },
        )
        return created_channel.id
