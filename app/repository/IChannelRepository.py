"""
This module defines the IChannelRepository interface.
"""

from abc import ABC, abstractmethod


class IChannelRepository(ABC):
    """
    Interface for channel repository.
    """

    @abstractmethod
    def get_channels(self):
        """
        Retrieve all channels.
        """

    @abstractmethod
    def get_channel_by_id(self, channel_id: int):
        """
        Retrieve a channel by its ID.
        """
