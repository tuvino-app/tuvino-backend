from fastapi import HTTPException

import uuid
import logging

from src.repository.base import BaseRepository, Session

from src.models.user import User
from src.repository.table_models.user import User as UserModel
from src.repository.table_models.user_preferences import UserPreference as PreferencesModel

class UsersRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_id(self, user_uid: str) -> User:
        try:
            uuid.UUID(user_uid)
        except ValueError:
            logging.error(f'El id {user_uid} no es un UUID valido')
            raise KeyError('Formato de ID de usuario invalido')

        user = self.session.query(UserModel).filter(UserModel.uid == user_uid).first()
        if not user:
            raise KeyError('El usuario no existe')
        return User(uid=user.uid, username=user.name, email=user.email)

    def save(self, user: User):
        logging.info(f'User: {user}')

        existing_user = self.session.get(UserModel, user.uid_to_str())

        if existing_user:
            existing_user.name = user.username
            existing_user.email = user.email
            existing_user.set_preferences(user.preferences)
        else:
            new_user = UserModel(uid=user.uid, name=user.username, email=user.email)
            new_user.set_preferences(user.preferences)
            self.session.add(new_user)

        self.session.commit()
        return user