from src.models.schemas.base import BaseSchemaModel
from typing import Optional
from pydantic import BaseModel, field_validator
import uuid

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

class WineFilters(BaseModel):
    wine_name: Optional[str] = None
    wine_type: Optional[str] = None
    winery: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    min_abv: Optional[float] = None
    max_abv: Optional[float] = None

    @field_validator('min_abv', 'max_abv', mode='before')
    @classmethod
    def parse_abv(cls, value):
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

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
    summary: str | None = None
    id: Optional[uuid.UUID] = None
    score: float | None = None
    harmonize_es: str | None = None

    def add_score(self, score: float):
        if score < 0.0 or score > 1.0:
            raise ValueError("Score must be a probability")
        self.score = round(score, 3)

class WineFavorites(BaseSchemaModel):
    id: int
    name: str
    type: str
    elaborate: str
    abv: float
    body: str
    country: str
    region: str
    winery: str

class WineTasted(BaseSchemaModel):
    id: int
    name: str
    type: str
    elaborate: str
    abv: float
    body: str
    country: str
    region: str
    winery: str
    rating: int | None