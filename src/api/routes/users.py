import fastapi
import logging

from fastapi import status, Depends, Path, HTTPException, Query
from src.api.dependencies import get_repository
from src.repository.users_repository import UsersRepository
from src.repository.preferences_repository import PreferencesRepository
from src.repository.wines_repository import WinesRepository
from src.repository.wine_recommendations_repository import WineRecommendationsRepository
from src.repository.ratings_repository import WineRatingsRepository

from src.models.schemas.user import UserPreferences, UserInfo, UserWineRating
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

@router.post(
    '/{user_id}/ratings',
    summary='Post user ratings',
    name='users:post-ratings',
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def post_user_rating(
    user_rating: UserWineRating,
    user_id: str = Path(..., title="The ID of the user posting the rating"),
    users_repo: UsersRepository = Depends(get_repository(repo_type=UsersRepository)),
    ratings_repo: WineRatingsRepository = Depends(get_repository(repo_type=WineRatingsRepository)),
):
    try:
        user = users_repo.get_user_by_id(user_id)
        rating = user.rate_wine(user_rating.wine_id, user_rating.rating)
        return ratings_repo.save(rating)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    '/{user_id}/favorites/{wine_id}',
    summary='Post user favorite wine',
    name='users:post-favorites',
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def post_user_favorite(
    user_id: str = Path(..., title="The ID of the user posting the favorite wine"),
    wine_id: int = Path(..., title="The ID of the wine marked as favorite"),
    users_repo: UsersRepository = Depends(get_repository(repo_type=UsersRepository))
):
    try:
        wines_repo = WinesRepository()
        user = users_repo.get_user_by_id(user_id)
        wine = wines_repo.get_by_id(wine_id)
        user.add_favorite(wine)
        users_repo.save(user)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    '/{user_id}/favorites/{wine_id}',
    summary='Delete user favorite wine',
    name='users:post-favorites',
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def delete_user_favorite(
    user_id: str = Path(..., title="The ID of the user deleting the favorite wine"),
    wine_id: int = Path(..., title="The ID of the wine marked as favorite"),
    users_repo: UsersRepository = Depends(get_repository(repo_type=UsersRepository))
):
    try:
        wines_repo = WinesRepository()
        user = users_repo.get_user_by_id(user_id)
        wine = wines_repo.get_by_id(wine_id)
        users_repo.delete_favorite_wine(user, wine)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))