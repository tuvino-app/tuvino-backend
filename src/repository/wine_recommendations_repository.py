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

    def get_recommendations(
        self,
        user: 'User',
        limit: int,
        wine_type: str = None,
        body: str = None,
        dryness: str = None,
        abv: float = None
    ) -> list:
        if not user.onboarding_completed:
            raise KeyError('User has not completed onboarding')

        wines_repo = WinesRepository()
        filtered_wines = []
        tried_ids = set()

        while len(filtered_wines) < limit:
            payload = {
                'type': user.favorite_type(),
                'body': user.favorite_body(),
                'dryness': user.favorite_dryness(),
                'abv': user.favorite_abv()
            }
            body_json = json.dumps(payload)
            logging.info(f'Payload enviado al modelo de recomendaciones: {body_json}')
            logging.info(f'Llamando a la API de recomendaciones en {self.model_api_url}')

            response = requests.post(f'{self.model_api_url}/wines', body_json, headers={'Content-Type': 'application/json'})
            logging.info(f'Llamada al modelo con parametros {body_json} devuelve: {response.text}')

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
                break  # No hay más recomendaciones

            new_found = False
            for wine_id_str in wine_ids:
                if wine_id_str in tried_ids:
                    continue
                tried_ids.add(wine_id_str)
                try:
                    wine = wines_repo.get_by_id(int(wine_id_str))
                    wine.add_score(scores_data.get(wine_id_str, 0))
                    if wine:
                        matches = True
                        if wine_type and (not hasattr(wine, "type") or wine.type.lower() != wine_type.lower()):
                            matches = False
                        if body and (not hasattr(wine, "body") or wine.body.lower() != body.lower()):
                            matches = False
                        if dryness and (not hasattr(wine, "dryness") or wine.dryness.lower() != dryness.lower()):
                            matches = False
                        if abv and (not hasattr(wine, "abv") or float(wine.abv) != float(abv)):
                            matches = False

                        if matches:
                            filtered_wines.append(wine)
                            new_found = True
                            if len(filtered_wines) >= limit:
                                break
                    else:
                        logging.warning(f'No se encontró el vino con ID: {wine_id_str}')
                except ValueError:
                    logging.error(f'ID de vino no válido: {wine_id_str}')
            if not new_found:
                break  # No se encontraron nuevos vinos que cumplan el filtro, termina el ciclo

        logging.info(f'Retorna {len(filtered_wines)} vinos tras aplicar filtros y límite')
        return filtered_wines[:limit]