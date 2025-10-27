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

    def get_recommendations(self, user: 'User', limit: int) -> list[dict]:
        if not user.onboarding_completed:
            raise KeyError('User has not completed onboarding')

        body = json.dumps({
            'type': user.favorite_type(),
            'body': user.favorite_body(),
            'dryness': user.favorite_dryness(),
            'abv': user.favorite_abv()
        })

        response = requests.post(f'{self.model_api_url}', body, headers={'Content-Type': 'application/json'})
        logging.info(f'Llamada al modelo con parametros {body} devuelve: {response.text}')

        if response.status_code != self.OK_STATUS_CODE:
            logging.error(
                f'Error al obtener recomendaciones de vinos. Status: {response.status_code}, Response: {response.text}')
            raise HTTPException(status_code=400, detail='Error al obtener recomendaciones de vinos')

        try:
            parsed_response_json = response.json()
            scores_data = parsed_response_json.get('scores', {})
            wine_ids = parsed_response_json.get('wines', {})

        except json.JSONDecodeError as e:
            logging.error(f'Error al decodificar la respuesta JSON del modelo: {e}')
            raise HTTPException(status_code=400, detail='Formato de respuesta de recomendación no válido')

        if not wine_ids:
            logging.info('El modelo no devolvió IDs de vino en la clave "scores".')
            return []

        wines = []
        wines_repo = WinesRepository()

        for wine_id_str in wine_ids:
            try:
                wine = wines_repo.get_by_id(int(wine_id_str))
                wine.add_score(scores_data.get(wine_id_str, 0))
                if wine:
                    wines.append(wine)
                else:
                    logging.warning(f'No se encontró el vino con ID: {wine_id_str}')
            except ValueError:
                logging.error(f'ID de vino no válido: {wine_id_str}')

        logging.info(f'Obtenidos {len(wines)} vinos')
        return wines