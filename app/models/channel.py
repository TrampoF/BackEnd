from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database_connection import Base


class Channel(Base):
    """
    Channel model represents the channels table in the database
    """

    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    chat_identifier = Column(String)
    api_key = Column(String)
    channel_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    profile = relationship("Profiles", foreign_keys=profile_id, back_populates="channels")
