"""
This module defines the User model.
"""

from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.DatabaseConnection import Base


class User(Base):
    """
    User model represents the users table in the database
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    channels = relationship("Channel", back_populates="user")
