from typing import List
from uuid import UUID
import datetime
from sqlalchemy.orm import Session
from app.models.channel import Channel
from app.models.tag import Tag
from app.repository.i_channel_repository import IChannelRepository
from app.schemas.create_channel_schema import CreateChannelSchema


class ChannelRepositoryDatabase(IChannelRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def create_channel(self, channel_data: CreateChannelSchema) -> Channel:
        channel_data = CreateChannelSchema(
            **channel_data.model_dump(),
        )
        channel = Channel(
            chat_identifier=channel_data.chat_identifier,
            channel_name=channel_data.channel_name,
            api_id=channel_data.api_id,
            api_hash=channel_data.api_hash,
            profile_id=channel_data.profile_id,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        for tag in channel_data.tags:
            new_tag = Tag(
                name=tag,
                profile_id=channel_data.profile_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            channel.tags.append(new_tag)
        self._session.add(channel)
        self._session.commit()
        return channel

    def get_channels(self) -> List[Channel]:
        return self._session.query(Channel).all()

    def get_channel_by_id(self, channel_id: UUID) -> Channel | None:
        return self._session.query(Channel).filter(Channel.id == channel_id).first()
