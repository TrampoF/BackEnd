from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.database.i_database_connection import IDatabaseConnection

Base = declarative_base()


class PostgresAdapter(IDatabaseConnection):
    """
    Adapter class for PostgreSQL database connection using SQLAlchemy.
    """

    def __init__(self):
        self._connection = create_engine("postgresql://postgres:123456@db:5432")
        self._session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self._connection
        )

    def get_db(self):
        db = self._session_local()
        try:
            yield db
        finally:
            db.close()
