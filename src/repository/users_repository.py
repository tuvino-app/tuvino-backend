from fastapi import HTTPException

import uuid
import logging

from src.repository.base import BaseRepository, Session

from src.models.user import User
from src.repository.table_models.user import User as UserModel

class UsersRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_id(self, user_uid: str) -> User:
        try:
            uuid.UUID(user_uid)
        except ValueError:
            logging.error(f'El id {user_uid} no es un UUID valido')
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        user = self.session.query(UserModel).filter(UserModel.uid == user_uid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User(uid=user.uid, username=user.name, email=user.email)
