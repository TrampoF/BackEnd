import os
import random
import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supabase import create_client
from app.application.get_channel import GetChannel
from app.application.register_channel import RegisterChannel
from app.application.register_profile import RegisterProfile
from app.repository.channel_repository_database import ChannelRepositoryDatabase
from app.repository.channel_repository_memory import ChannelRepositoryMemory
from app.repository.profile_repository_database import ProfileRepositoryDatabase
from app.repository.profile_repository_memory import ProfileRepositoryMemory
from app.repository.profile_repository_supabase import ProfileRepositorySupabase
from app.repository.tag_repository_database import TagRepositoryDatabase
from app.repository.tag_repository_memory import TagRepositoryMemory


@pytest.fixture()
def db():
    """
    Fixture for database connection.
    """
    connection = create_engine(
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@{os.getenv('DB_HOST', '127.0.0.1')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'postgres')}"
    )
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    return session_local()


@pytest.fixture()
def supabase():
    """
    Fixture for Supabase database connection.
    """
    client = create_client(
        os.getenv("SUPABASE_URL", "http://localhost:5432"),
        os.getenv("SUPABASE_KEY", "postgres"),
    )
    return client


@pytest.fixture()
def repositories(db, supabase):
    return {
        "channel_repository": ChannelRepositoryDatabase(session=db),
        "tag_repository": TagRepositoryDatabase(session=db),
        "profile_repository": ProfileRepositorySupabase(client=supabase),
    }


class TestRegisterChannel:
    def test_should_register_channel(self, repositories):
        profile_data = {
            "first_name": "Foo",
            "last_name": "Bar",
            "email": f"foo{random.random()}@bar.com",
            "password": "password",
            "password_confirmation": "password",
        }
        registered_profile_id = RegisterProfile(
            profile_repository=repositories["profile_repository"]
        ).execute(profile_data)

        channel_data1 = {
            "channel_name": "Lorem Ipsum",
            "profile_id": registered_profile_id,
            "tags": ["CSS", "HTML", "PHP"],
            "chat_identifier": "https://t.me/s/CafeinaVagas",
        }
        registered_channel1_id = RegisterChannel(
            channel_repository=repositories["channel_repository"],
            tag_repository=repositories["tag_repository"],
        ).execute(channel_data=channel_data1)
        registered_channel1 = GetChannel(
            channel_repository=repositories["channel_repository"]
        ).execute(channel_id=registered_channel1_id)
        assert registered_channel1_id == registered_channel1.id
        assert channel_data1["channel_name"] == registered_channel1.channel_name
        assert uuid.UUID(channel_data1["profile_id"]) == registered_channel1.profile_id
        assert channel_data1["chat_identifier"] == registered_channel1.chat_identifier
        assert channel_data1["tags"] == registered_channel1.tags
        channel_data2 = {
            "channel_name": "Lorem Ipsum",
            "profile_id": registered_profile_id,
            "tags": ["PHP", "Laravel", "PostgreSQL"],
            "chat_identifier": "https://t.me/s/CafeinaVagas",
        }
        registered_channel2_id = RegisterChannel(
            channel_repository=repositories["channel_repository"],
            tag_repository=repositories["tag_repository"],
        ).execute(channel_data=channel_data2)
        registered_channel2 = GetChannel(
            channel_repository=repositories["channel_repository"]
        ).execute(channel_id=registered_channel2_id)
        assert registered_channel2_id == registered_channel2.id
        assert channel_data2["channel_name"] == registered_channel2.channel_name
        assert uuid.UUID(channel_data2["profile_id"]) == registered_channel2.profile_id
        assert channel_data2["chat_identifier"] == registered_channel2.chat_identifier
        assert channel_data2["tags"] == registered_channel2.tags
