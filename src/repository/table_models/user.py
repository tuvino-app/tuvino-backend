from email.policy import default

from sqlalchemy import select, Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.repository.config.table import Base
from src.repository.table_models.user_preferences import UserPreference

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
    onboarding_completed = Column(Boolean, nullable=False, default=False)
    preferences = relationship("UserPreference", back_populates="user")

    def set_preferences(self, preferences: list):
        for user_preference in preferences:
            self.preferences.append(UserPreference(user_id=self.uid, option_id=user_preference.id))
        self.onboarding_completed = True

    def uid_to_str(self):
        return str(self.uid)