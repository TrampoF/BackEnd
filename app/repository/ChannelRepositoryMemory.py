"""
This module contains the ChannelRepository class which implements the IChannelRepository interface.
"""

from typing import List
from app.models.Channel import Channel
from app.repository.IChannelRepository import IChannelRepository


class ChannelRepositoryMemory(IChannelRepository):
    """
    ChannelRepository implements the IChannelRepository
    interface for channel-related memory operations.
    """

    _channels: List[Channel]

    def __init__(self):
        self._channel = []

    def get_channels(self):
        return self._channel

    def get_channel_by_id(self, channel_id: int):
        channel = next(
            (channel for channel in self._channel if channel.id == channel_id), None
        )
        return channel

    def create_channel(self, channel_data: dict):
        self._channels.append(Channel(**channel_data))
