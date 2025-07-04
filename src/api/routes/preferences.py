import fastapi

router = fastapi.APIRouter(prefix="/preferences", tags=["preferences"])

@router.get('/')
async def get_preferences():
    return {'message': 'Preferences'}