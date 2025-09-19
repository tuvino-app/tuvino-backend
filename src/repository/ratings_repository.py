import logging
import uuid

from sqlalchemy import select

from src.repository.base import BaseRepository, Session
from src.models.rating import Rating
from src.repository.table_models.wine_ratings import WineRating as WineRatingModel

class WineRatingsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_user_id_and_wine_id(self, user_id: str, wine_id: int):
        return self.session.execute(
            select(WineRatingModel).where(
                WineRatingModel.user_id == user_id,
                WineRatingModel.wine_id == wine_id
            )
        ).scalars().first()

    def save(self, rating: Rating):
        original_rating = self.get_by_user_id_and_wine_id(str(rating.user_id), rating.wine_id)
        if original_rating:
            original_rating.rating = rating.rating
        else:
            self.session.add(WineRatingModel(
                user_id=str(rating.user_id),
                wine_id=rating.wine_id,
                rating=rating.rating,
            ))

        return self.session.commit()