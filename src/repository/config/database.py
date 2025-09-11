from supabase import create_client, Client
from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from src.config.manager import settings


class Database:
    def __init__(self):
        self.postgres_uri = str(PostgresDsn(settings.DB_POSTGRES_URI))

        self.supabase: Client = create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_KEY
        )

        self.engine = create_engine(
            url=self.postgres_uri,
            poolclass=QueuePool,
        )

        self.sessionmaker = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )

    def test_connection(self):
        try:
            # Probar conexión con Supabase
            response = self.supabase.table('users').select("*").limit(1).execute()
            print("✅ Conexión exitosa a Supabase!")
            return True
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False


# Initialize database connection
db = Database()