from fastapi import Depends
from sqlalchemy.orm import Session


from app.database.database_connection import PostgresAdapter
from app.models.channel import Channel
from app.repository.ichannel_repository import IChannelRepository


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
