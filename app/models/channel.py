import datetime
from uuid import UUID
from sqlalchemy import (
    ForeignKey,
)
from typing import (
    List,
    TYPE_CHECKING,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.database.database_connection import Base

if TYPE_CHECKING:
    from app.models.tag import Tag
    from app.models.tags_channels import TagsChannels


class Channel(Base):
    """
    Channel model represents the channels table in the database
    """

    __tablename__ = "channels"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default="uuid_generate_v4()",
    )
    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profiles.id"))
    chat_identifier: Mapped[str]
    channel_name: Mapped[str]
    api_id: Mapped[str]
    api_hash: Mapped[str]
    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]

    tags_channels: Mapped[List["TagsChannels"]] = relationship(back_populates="channel")
    tags: AssociationProxy[List["Tag"]] = association_proxy(
        "tags_channels",
        "tag",
        creator=lambda tag_obj: TagsChannels(tag=tag_obj),
    )


from app.models.tags_channels import TagsChannels
