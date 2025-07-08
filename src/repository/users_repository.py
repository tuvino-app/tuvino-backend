from fastapi import HTTPException

import uuid
import logging

from src.repository.base import BaseRepository, Session

from src.models.user import User

class UsersRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_id(self, user_uid: str) -> User:
        try:
            uuid.UUID(user_uid)
        except ValueError:
            logging.error(f'El id {user_uid} no es un UUID valido')
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        return self.session.query(User).filter(User.uid == user_uid).first()
