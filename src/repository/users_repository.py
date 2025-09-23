from fastapi import HTTPException

import uuid
import logging

from src.repository.base import BaseRepository, Session

from src.models.wine import Wine
from src.models.user import User
from src.models.rating import Rating
from src.repository.table_models import User as UserModel, FavoriteWines, Wine as WineModel, WineRating as WineRatingModel
from src.repository.preferences_repository import PreferencesRepository
from src.repository.ratings_repository import WineRatingsRepository

class UsersRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_user_by_id(self, user_uid: str) -> User:
        try:
            uuid.UUID(user_uid)
        except ValueError:
            logging.error(f'El id {user_uid} no es un UUID valido')
            raise KeyError('Formato de ID de usuario invalido')

        user_row = self.session.query(UserModel).filter(UserModel.uid == user_uid).first()
        if not user_row:
            raise KeyError('El usuario no existe')
        user = User(uid=user_row.uid, username=user_row.name, email=user_row.email)
        if user_row.onboarding_completed:
            user.onboarding_completed = True
        user.add_preferences(PreferencesRepository(self.session).get_preferences(user.uid))
        user.set_favorites(self.get_favorite_wines(user))
        user.set_ratings(WineRatingsRepository(self.session).get_by_user_id(user_id=user.uid_to_str()))
        return user

    def get_favorite_wines(self, user: User):
        favorites = self.session.query(WineModel).join(FavoriteWines, WineModel.wine_id == FavoriteWines.wine_id).filter(FavoriteWines.user_id == user.uid_to_str()).order_by(FavoriteWines.added_date.desc()).all()
        wines = []
        for wine in favorites:
            wines.append(Wine(wine.wine_id, wine.wine_name, wine.type, wine.elaborate, wine.abv, wine.body, wine.country, wine.region, wine.winery))
        return wines

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

        favorites = [favorite.id for favorite in self.get_favorite_wines(user)]
        for favorite in user.get_favorites():
            if favorite.id not in favorites:
                logging.info(f'New favorite detected: {favorite} saving...')
                self.session.add(FavoriteWines(user_id=user.uid_to_str(), wine_id=favorite.wine_id))

        self.session.commit()
        return user

    def delete_favorite_wine(self, user: User, wine_id):
        favorite_ids = [fav.id for fav in user.get_favorites()]
        if wine_id not in favorite_ids:
            raise ValueError('Wine not in favorites')

        self.session.query(FavoriteWines).filter(FavoriteWines.user_id == user.uid_to_str(), FavoriteWines.wine_id == wine_id).delete()
        self.session.commit()