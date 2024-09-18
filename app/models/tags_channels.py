from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.database.database_connection import Base
from app.models.channel import Channel

if TYPE_CHECKING:
    from app.models.tag import Tag


class TagsChannels(Base):
    __tablename__ = "tags_channels"

    channel_id: Mapped[UUID] = mapped_column(
        ForeignKey("channels.id"), primary_key=True
    )

    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"), primary_key=True)

    channel: Mapped[Channel] = relationship(back_populates="tags_channels")

    tag: Mapped["Tag"] = relationship()
