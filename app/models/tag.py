from uuid import UUID
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database.database_connection import Base


class Tag(Base):

    __tablename__ = "tags"
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        nullable=False,
        server_default="uuid_generate_v4()",
    )
    name: Mapped[str] = mapped_column(nullable=False)
    profile_id: Mapped[UUID] = mapped_column(ForeignKey("profiles.id"), nullable=False)
    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]
