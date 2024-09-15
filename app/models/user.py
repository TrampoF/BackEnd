from sqlalchemy import UUID, DateTime, Column, String
from sqlalchemy.orm import relationship

from app.database.database_connection import Base


class User(Base):
    """
    User model represents the users table in the database
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    channels = relationship("Channel", back_populates="user")
