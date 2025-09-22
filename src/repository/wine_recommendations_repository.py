import os
import logging
from fastapi.exceptions import HTTPException
import json
from src.repository.wines_repository import WinesRepository

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
        if not user.onboarding_completed:
            raise KeyError('User has not completed onboarding')
        body = json.dumps({
            'type': user.favorite_type(),
            'body': user.favorite_body(),
            'dryness': user.favorite_dryness(),
            'abv': user.favorite_abv()
        })
        response = requests.post(f'{self.model_api_url}', body, headers={'Content-Type': 'application/json'})
        logging.info(f'Llamada al modelo con parametros {body} devuelve: {response}')
        if response.status_code != self.OK_STATUS_CODE:
            logging.error(f'Error al obtener recomendaciones de vinos')
            raise HTTPException(status_code=400, detail='Error al obtener recomendaciones de vinos')
        parsed_response = response.text.strip('[]\n').replace(' ', '').replace('"', '')
        wine_ids = parsed_response.split(',')
        wines = []
        wines_repo = WinesRepository()
        for wine_id in wine_ids[:limit]:
            wines.append(wines_repo.get_by_id(int(wine_id)))
        logging.info(f'Vinos: {wines}')
        return wines