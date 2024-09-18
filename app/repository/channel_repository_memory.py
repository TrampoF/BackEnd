import datetime
from typing import List
import uuid
from app.models.channel import Channel
from app.repository.i_channel_repository import IChannelRepository
from app.schemas.create_channel_schema import CreateChannelSchema


class ChannelRepositoryMemory(IChannelRepository):
    """
    ChannelRepositoryMemory implements the IChannelRepository
    interface for channel-related memory operations.
    """

    _channels = List[Channel]

    def __init__(self):
        self._channels = []

    def get_channels(self) -> List[Channel]:
        return self._channels

    def get_channel_by_id(self, channel_id: uuid.UUID) -> Channel | None:
        return next(
            (channel for channel in self._channels if channel.id == channel_id), None
        )

    def create_channel(self, channel_data: CreateChannelSchema) -> Channel:
        channel_data = CreateChannelSchema(
            **channel_data.model_dump(),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        channel = Channel(**channel_data.model_dump(), id=uuid.uuid4())
        self._channels.append(channel)
        return channel
