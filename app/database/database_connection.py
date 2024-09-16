import os

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
        self._connection = create_engine(
            "postgresql://%s:%s@%s:%s/%s"
            % (
                os.getenv("DB_USER", "postgres"),
                os.getenv("DB_PASSWORD", "postgres"),
                os.getenv("DB_HOST", "127.0.0.1"),
                os.getenv("DB_PORT", "5432"),
                os.getenv("DB_NAME", "postgres"),
            )
        )
        self._session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self._connection
        )

    def get_db(self):
        db = self._session_local()
        try:
            return db
        finally:
            db.close()