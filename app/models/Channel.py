"""
This module defines the Channel model.
"""

from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.DatabaseConnection import Base


class Channel(Base):
    """
    Channel model represents the channels table in the database
    """

    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chat_identifier = Column(String)
    api_key = Column(String)
    channel_name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_at = Column(DateTime, nullable=True)
    user = relationship("User", foreign_keys=user_id, back_populates="channels")
