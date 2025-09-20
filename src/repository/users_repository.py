from fastapi import HTTPException

import uuid
import logging

from src.models.wine import Wine
from src.repository.base import BaseRepository, Session

from src.models.user import User
from src.repository.table_models import User as UserModel, FavoriteWines
from src.repository.preferences_repository import PreferencesRepository
from src.repository.wines_repository import WinesRepository


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
        user = User(uid=user.uid, username=user.name, email=user.email)
        user.add_preferences(PreferencesRepository(self.session).get_preferences(user.uid))
        user.favorites = self.session.query(FavoriteWines).filter(FavoriteWines.user_id == user.uid_to_str()).all()
        return user



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

        saved_favorites = self.session.query(FavoriteWines).filter(FavoriteWines.user_id == user.uid_to_str()).all()
        favorites = [favorite.wine_id for favorite in saved_favorites]
        for favorite in user.get_favorites():
            if favorite.wine_id not in favorites:
                logging.info(f'New favorite detected: {favorite} saving...')
                self.session.add(FavoriteWines(user_id=user.uid_to_str(), wine_id=favorite.wine_id))

        self.session.commit()
        return user

    def delete_favorite_wine(self, user: User, wine):
        favorite_ids = [fav.wine_id for fav in user.get_favorites()]
        if wine.wine_id not in favorite_ids:
            raise ValueError('Wine not in favorites')

        self.session.query(FavoriteWines).filter(FavoriteWines.user_id == user.uid_to_str(), FavoriteWines.wine_id == wine.wine_id).delete()
        self.session.commit()