import fastapi
from fastapi import Depends
from src.repository.wines_repository import WinesRepository

router = fastapi.APIRouter(prefix="/preferences", tags=["preferences"])

@router.get('/')
async def get_preferences(
    wines_repo = Depends(WinesRepository),
):
    return wines_repo.get_wine_preference_options()
