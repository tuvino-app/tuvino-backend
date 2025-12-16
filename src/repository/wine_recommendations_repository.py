import os
import logging
from fastapi.exceptions import HTTPException
import json
from src.repository.wines_repository import WinesRepository
from src.services.user_features_service import UserFeaturesService

import requests

from src.models.user import User

class WineRecommendationsRepository:
    def __init__(self):
        self.OK_STATUS_CODE = 200
        self.model_api_url = os.getenv('RECOMMENDATIONS_API_URL')
        if not self.model_api_url:
            logging.error('No se encuentra la URL de la API de recomendaciones de vinos')
            raise KeyError('No se encuentra la URL de la API de recomendaciones de vinos')
        
        self.features_service = UserFeaturesService()

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

        # Step 1: Gather user's rating history data
        logging.info(f'Gathering rating data for user {user.uid_to_str()}')
        
        wines_repo = WinesRepository()  # Needed later for fetching recommended wines
        
        # Get user's ratings - they already have wine details attached
        user_ratings = user.get_ratings()

        logging.info(f'User ratings: {user_ratings}')
        
        # Build rating data with wine attributes
        ratings_data = []
        for rating in user_ratings:
            try:
                ratings_data.append({
                    'wine_id': rating.wine_id,
                    'rating': rating.rating,
                    'wine_type': rating.wine.type if hasattr(rating.wine, 'type') else None,
                    'body': rating.wine.body if hasattr(rating.wine, 'body') else None,
                    'abv': rating.wine.abv if hasattr(rating.wine, 'abv') else None,
                    'country': rating.wine.country if hasattr(rating.wine, 'country') else None,
                    'grape': rating.wine.elaborate if hasattr(rating.wine, 'elaborate') else None,
                    'acidity': rating.wine.acidity if hasattr(rating.wine, 'acidity') else None,
                    'complexity': 0,  # Not in current schema - could be calculated from wine attributes
                    'is_reserve': False,  # Not in current schema
                    'is_grand': False,  # Not in current schema
                    'created_at': None,  # Not available in current Rating model
                })
            except Exception as e:
                logging.warning(f'Could not process rating: {e}')
                continue
        
        # Step 2: Calculate user features
        logging.info(f'Calculating features for user {user.uid_to_str()} with {len(ratings_data)} ratings')
        user_features = self.features_service.calculate_features(
            user_id=user.uid_to_str(),
            ratings_data=ratings_data,
            preferences_data=user.preferences if hasattr(user, 'preferences') else None
        )
        
        # Step 3: Call the Two Tower Model with 55 features + user_id
        logging.info(f'Calling Two Tower Model with {len(user_features)} features')
        payload = {
            'user_id': user.uid_to_str(),  # Include user_id for future requirements
            **user_features  # All 55 features
        }
        body_json = json.dumps(payload)
        
        logging.info(f'Payload enviado al modelo (primeros 5 features): {dict(list(payload.items())[:5])}...')
        logging.info(f'Llamando a la API de recomendaciones en {self.model_api_url}/wines')

        response = requests.post(
            f'{self.model_api_url}/wines', 
            body_json, 
            headers={'Content-Type': 'application/json'}
        )
        logging.info(f'Llamada al modelo devuelve status: {response.status_code}')

        if response.status_code != self.OK_STATUS_CODE:
            logging.error(
                f'Error al obtener recomendaciones de vinos. Status: {response.status_code}, Response: {response.text}')
            raise HTTPException(status_code=400, detail='Error al obtener recomendaciones de vinos')

        # Step 4: Process response
        try:
            parsed_response_json = response.json()
            scores_data = parsed_response_json.get('scores', {})
            wine_ids = parsed_response_json.get('wines', [])
        except json.JSONDecodeError as e:
            logging.error(f'Error al decodificar la respuesta JSON del modelo: {e}')
            raise HTTPException(status_code=400, detail='Formato de respuesta de recomendación no válido')

        if not wine_ids:
            logging.info('El modelo no devolvió IDs de vino.')
            return []

        # Step 5: Apply filters and build response
        filtered_wines = []
        tried_ids = set()

        for wine_id_str in wine_ids:
            if wine_id_str in tried_ids or len(filtered_wines) >= limit:
                continue
            
            tried_ids.add(wine_id_str)
            
            try:
                wine = wines_repo.get_by_id(int(wine_id_str))
                if wine:
                    wine.add_score(scores_data.get(wine_id_str, 0))
                    
                    # Apply optional filters
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
                else:
                    logging.warning(f'No se encontró el vino con ID: {wine_id_str}')
            except ValueError:
                logging.error(f'ID de vino no válido: {wine_id_str}')
            except Exception as e:
                logging.error(f'Error processing wine {wine_id_str}: {e}')

        logging.info(f'Retorna {len(filtered_wines)} vinos tras aplicar filtros y límite')
        return filtered_wines[:limit]