import fastapi
import random

from fastapi import status
from repository.users_repository import UsersRepository

router = fastapi.APIRouter(prefix="/users", tags=["users"])

wines = [
    'Reserva Chardonnay',
    'Merlot Reserve Trocken',
    'Los Cardos Malbec',
    'Pinot Noir',
    'Premiere Napa Valley Cabernet Sauvignon',
    'Château Chemin Royal Moulis-en-Médoc',
    'Cabernet Sauvignon'
]

@router.get(
    '/{user_id}/recommendations',
    summary='Get recommendations for a user',
    name='users:get-recommendations',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def get_recommendations(user_id: int):
    return {
        'userId': user_id,
        'recommendations': random.sample(wines, 3)
    }

@router.get(
    '/{user_id}',
    summary='Get recommendations for a user',
    name='users:get-recommendations',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def get_user_info(user_id: int):
    users_repo = UsersRepository()
    # response = users_repo.get_user_by_id(user_id)
    return users_repo.get_all_users()
