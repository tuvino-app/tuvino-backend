from src.models.schemas.base import BaseSchemaModel

class UserPreferences(BaseSchemaModel):
    age_range: int

class UserInfo(BaseSchemaModel):
    uid: str
    username: str
    email: str