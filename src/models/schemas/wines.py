from src.models.schemas.base import BaseSchemaModel
from typing import Optional
import uuid

class WineSchema(BaseSchemaModel):
    wine_id: int
    wine_name: str
    type: str
    elaborate: str
    grapes: str
    harmonize: str
    abv: float
    body: str
    acidity: str
    country: str
    region: str
    winery: str
    vintages: str
    id: Optional[uuid.UUID] = None