import uuid
from sqlalchemy import UUID, DateTime, Column, String
from sqlalchemy.orm import relationship

from app.database.database_connection import Base
from app.models.channel import Channel


class Profile(Base):
    """
    Profile model represents the profiles table in the database
    """

    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    channels = relationship("Channel", backref="profile")
