import os
from supabase import Client, create_client
from app.database.i_database_connection import IDatabaseConnection


class SupabaseAdapter(IDatabaseConnection):
    _client: Client
    def __init__(self):
        self._client = create_client(
            os.getenv("SUPABASE_URL", "http://localhost:5432"),
            os.getenv("SUPABASE_KEY", "postgres"),
        )

    def get_db(self):
        yield self._client
