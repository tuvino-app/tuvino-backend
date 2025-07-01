import fastapi
from api.routes.users import router as users_router

router = fastapi.APIRouter()

router.include_router(router=users_router)