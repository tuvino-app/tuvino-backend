import fastapi
from fastapi import Depends, status

from src.models.schemas.preference import PreferenceAttributes
from src.api.dependencies import get_repository
from src.repository.preferences_repository import PreferencesRepository

router = fastapi.APIRouter(prefix="/preferences", tags=["preferences"])

@router.get(
    '/',
    summary='Get options to preferences, listed per type',
    name='preferences:get-options',
    response_model=PreferenceAttributes,
    status_code=status.HTTP_200_OK,
)
async def get_preferences(
    preferences_repo = Depends(get_repository(repo_type=PreferencesRepository)),
):
    preferences = preferences_repo.get_options()
    preferences_by_category = {}
    for preference in preferences:
        category_key = preference.category.name

        if category_key not in preferences_by_category:
            preferences_by_category[category_key] = {}

        preferences_by_category[category_key][preference.id] = preference.get_option_and_description()

    return preferences_by_category