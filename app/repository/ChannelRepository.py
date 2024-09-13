"""
This module contains the ChannelRepository class which implements the IChannelRepository interface.
"""

from fastapi import Depends
from sqlalchemy.orm import Session


from app.database.DatabaseConnection import PostgresAdapter
from app.models.Channel import Channel
from app.repository.IChannelRepository import IChannelRepository


class ChannelRepository(IChannelRepository):
    """
    ChannelRepository implements the IChannelRepository
    interface for channel-related database operations.
    """

    def __init__(self, session: Session = Depends(PostgresAdapter().get_db)):
        self._session = session

    def get_channels(self):
        channels = self._session.query(Channel).all()
        return channels

    def get_channel_by_id(self, channel_id: int):
        channel = self._session.query(Channel).filter(Channel.id == channel_id).first()
        return channel
