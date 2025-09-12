import fastapi
import logging

from fastapi import status, Depends, Path, HTTPException, Query
from src.api.dependencies import get_repository
from src.repository.users_repository import UsersRepository
from src.repository.preferences_repository import PreferencesRepository
from src.repository.wine_recommendations_repository import WineRecommendationsRepository

from src.models.schemas.user import UserPreferences, UserInfo
from src.models.schemas.recommendations import WineRecommendations

router = fastapi.APIRouter(prefix="/users", tags=["users"])

@router.get(
    '/recommendations',
    summary='Get wine recommendations for a specific user',
    name='recommendations:get-user-recommendations',
    response_model=WineRecommendations,
    status_code=status.HTTP_200_OK,
)
async def get_wine_recommendations(
    user_id: str = Query(..., description="ID of the user to get recommendations for"),
    limit: int = Query(3, description="Maximum number of recommendations to return", ge=1, le=20),
    users_repo: UsersRepository = Depends(get_repository(repo_type=UsersRepository)),
    preferences_repo: PreferencesRepository = Depends(get_repository(repo_type=PreferencesRepository)),
):
    try:
        recommendations_repo = WineRecommendationsRepository()
        user = users_repo.get_user_by_id(user_id)
        recommended_wines = recommendations_repo.get_recommendations(user, limit)
        return WineRecommendations(
            user_id=user_id,
            recommendations=recommended_wines
        )
    except KeyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    '/{user_id}',
    summary='Get information for a user',
    name='users:get-info',
    response_model=UserInfo,
    status_code=status.HTTP_200_OK,
)
async def get_user_info(
    user_id: str = Path(..., title="The ID of the account to get the info"),
    users_repo: UsersRepository = Depends(get_repository(repo_type=UsersRepository)),
):
    try:
        user = users_repo.get_user_by_id(user_id)
        return UserInfo(uid=user.uid_to_str(), username=user.username, email=user.email)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

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
    users_repo: UsersRepository = Depends(get_repository(repo_type=UsersRepository)),
):
    try:
        user = users_repo.get_user_by_id(user_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    user.add_preferences(user_preferences)
    return users_repo.save(user)
