import fastapi

from src.api.routes.users import router as users_router
from src.api.routes.preferences import router as preferences_router

default_router = fastapi.APIRouter()
router = fastapi.APIRouter()

@default_router.get('/')
async def get_app_info():
    return {
        'appName': 'tuVino',
        'version': '0.0.1',
    }

router.include_router(router=users_router)
router.include_router(router=preferences_router)