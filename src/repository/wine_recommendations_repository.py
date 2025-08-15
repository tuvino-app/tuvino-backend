import os
import logging
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
        response = requests.post(f'{self.model_api_url}?limit={limit}')
        logging.info(f'Llamada al modelo devuelve: {response}')
        if response.status_code != self.OK_STATUS_CODE:
            logging.error(f'Error al obtener recomendaciones de vinos')
            raise Exception(f'Error al obtener recomendaciones de vinos')
        return response.json()