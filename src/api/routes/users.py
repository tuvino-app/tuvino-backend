import fastapi
import random

from fastapi import status, Depends, Path
from repository.users_repository import UsersRepository

from models.schemas.user import *

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
async def get_recommendations(
    user_id: int = Path(..., title="The ID of the account to get the recommendations for")
):
    return {
        'userId': user_id,
        'recommendations': random.sample(wines, 3)
    }

@router.get(
    '/{user_id}',
    summary='Get information for a user',
    name='users:get-info',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def get_user_info(
    user_id: str = Path(..., title="The ID of the account to get the info"),
    users_repo: UsersRepository = Depends(UsersRepository),
):
    return users_repo.get_user_by_id(user_id)

@router.post(
    '/{user_id}',
    summary='Post user preferences',
    name='users:post-preferences',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def update_user_preferences(
    user_preferences: UserPreferences,
    user_id: str = Path(..., title="The ID of the account to update"),
    users_repo: UsersRepository = Depends(UsersRepository),
):
    return users_repo.get_user_by_id(user_id)
