from uuid import UUID

from pydantic import BaseModel
from app.repository.i_channel_repository import IChannelRepository


class Output(BaseModel):
    id: UUID
    channel_name: str
    profile_id: UUID
    chat_identifier: str
    tags: list[str]


class GetChannel:

    _channel_repository: IChannelRepository

    def __init__(self, channel_repository: IChannelRepository):
        self._channel_repository = channel_repository

    def execute(self, channel_id: UUID) -> Output | None:
        existing_channel = self._channel_repository.get_channel_by_id(channel_id)
        tags = [tag.name for tag in existing_channel.tags]
        channel = Output(
            id=existing_channel.id,
            channel_name=existing_channel.channel_name,
            profile_id=existing_channel.profile_id,
            chat_identifier=existing_channel.chat_identifier,
            tags=tags,
        )
        return channel
