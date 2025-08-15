from src.models.schemas.base import BaseSchemaModel

class WineRecommendations(BaseSchemaModel):
    user_id: str
    recommendations: list
    metadata: dict

"""
input: {RECOMMENDATIONS_API_URL}?limit=5
{
  "type": 'Red',
  "body": 'Medium-bodied',
  "intensity": 'Low',
  "dryness": 2,
  "abv": 11.2
}
output: {
  "user_id": "a5031c00-9c10-4b46-8b95-9c75cc5715a9",
  "recommendations": [
    {
      "wine_id": "169135",
      "wine_name": "Fratello",
      "winery": "SuperUco",
      "varietal": "Malbec",
      "vintage": 2018,
      "compatibility_score": 0.92,
      "reason": "Basado en tu preferencia por vinos tintos de cuerpo completo"
    },
    {
      "wine_id": "169135",
      "wine_name": "Fratello",
      "winery": "SuperUco",
      "varietal": "Malbec",
      "vintage": 2018,
      "compatibility_score": 0.89,
      "reason": "Basado en tu preferencia por vinos tintos de cuerpo completo"
    }
  ],
  "metadata": {
    "generated_at": "2023-11-15T14:30:00Z",
    "model_version": "v3.1.0"
  }
}


"""