from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.models.channel import Channel
from app.schemas.create_channel_schema import CreateChannelSchema


class IChannelRepository(ABC):
    """
    Interface for channel repository.
    """

    @abstractmethod
    def get_channels(self) -> List[Channel]:
        """
        Retrieve all channels.
        """

    @abstractmethod
    def get_channel_by_id(self, channel_id: UUID) -> Channel:
        """
        Retrieve a channel by its ID.
        """

    @abstractmethod
    def create_channel(self, channel_data: CreateChannelSchema) -> Channel:
        """
        Create a new channel.
        """
