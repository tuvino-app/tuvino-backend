from src.models.schemas.base import BaseSchemaModel
from typing import Optional

class WineBase(BaseSchemaModel):
    id: str
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

class WineFilters(BaseSchemaModel):
    type: Optional[str] = None
    body: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    winery: Optional[str] = None
    grapes: Optional[str] = None