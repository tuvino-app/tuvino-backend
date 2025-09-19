import logging
import uuid

from sqlalchemy import select

from src.repository.base import BaseRepository, Session
from src.models.rating import Rating
from src.repository.table_models.wine_ratings import WineRating as WineRatingModel

class WineRatingsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def save(self, rating: Rating):
        self.session.add(WineRatingModel(
            user_id=str(rating.user_id),
            wine_id=rating.wine_id,
            rating=rating.rating,
        ))

        return self.session.commit()