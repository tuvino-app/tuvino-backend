from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from src.config.manager import settings


class Database:
    def __init__(self):
        # Inicializar cliente Supabase
        self.supabase: Client = create_client(
            supabase_url=settings.DB_POSTGRES_HOST,
            supabase_key=settings.DB_POSTGRES_PASSWORD
        )
        
        # Construir URI para SQLAlchemy
        db_url = self.supabase.postgrest.from_("users").url
        db_url = db_url.replace("/rest/v1", "")  # Ajustar URL
        
        self.engine = create_engine(
            url=db_url,
            poolclass=QueuePool,
            connect_args={
                "sslmode": "require",
                "headers": {"apikey": settings.DB_POSTGRES_PASSWORD}
            }
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