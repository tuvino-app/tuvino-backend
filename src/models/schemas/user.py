from src.models.schemas.base import BaseSchemaModel

class UserPreferences(BaseSchemaModel):
    type: int
    body: int
    intensity: int
    dryness: int
    abv: int

class UserInfo(BaseSchemaModel):
    uid: str
    username: str
    email: str