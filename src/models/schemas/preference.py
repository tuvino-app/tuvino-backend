from src.models.schemas.base import BaseSchemaModel

class PreferenceAttributes(BaseSchemaModel):
    types: dict[int, str]
    bodies: dict[int, str]
    intensities: dict[int, str]
    dryness: dict[int, str]
    abv: dict[int, str]