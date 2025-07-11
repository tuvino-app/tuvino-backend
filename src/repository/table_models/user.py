from sqlalchemy import select, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.repository.config.table import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        nullable=False
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)