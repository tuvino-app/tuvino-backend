from pydantic import EmailStr
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

class UserWineRating(BaseSchemaModel):
    wine: int
    rating: int | None = None

class UserFavoriteWines(BaseSchemaModel):
    favorite_wines: list
    tasted_wines: list

class UserCreate(BaseSchemaModel):
    email: EmailStr
    password: str

class UserLogin(BaseSchemaModel):
    email: EmailStr
    password: str