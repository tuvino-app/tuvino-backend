from src.models.schemas.base import BaseSchemaModel

class UserPreferences(BaseSchemaModel):
    type: int
    body: int
    intensity: int
    dryness: int
    abv: int

    def list_values(self):
        return [self.type, self.body, self.intensity, self.dryness, self.abv]

class UserInfo(BaseSchemaModel):
    uid: str
    username: str
    email: str
    ratings: list

class UserWineRating(BaseSchemaModel):
    wine_id: int
    rating: int | None = None

class UserFavoriteWines(BaseSchemaModel):
    wines: list