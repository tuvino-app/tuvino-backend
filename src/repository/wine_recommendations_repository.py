import os
import logging
from fastapi.exceptions import HTTPException

import requests

from src.models.user import User

class WineRecommendationsRepository:
    def __init__(self):
        self.OK_STATUS_CODE = 200
        self.model_api_url = os.getenv('RECOMMENDATIONS_API_URL')
        if not self.model_api_url:
            logging.error('No se encuentra la URL de la API de recomendaciones de vinos')
            raise KeyError('No se encuentra la URL de la API de recomendaciones de vinos')

    def get_recommendations(self, user: User, limit: int) -> list[dict]:
        response = requests.get(f'{self.model_api_url}?limit={limit}')
        # response = requests.post(f'{self.model_api_url}?limit={limit}') TODO: Agregar como parámetros las preferencencias del usuario cuando se deje de mockear el modelo
        logging.info(f'Llamada al modelo devuelve: {response}')
        if response.status_code != self.OK_STATUS_CODE:
            logging.error(f'Error al obtener recomendaciones de vinos')
            raise HTTPException(status_code=400, detail='Error al obtener recomendaciones de vinos')
        return response.json()