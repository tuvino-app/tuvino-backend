import fastapi
from fastapi import FastAPI, Request, Form

from routes.users import router as users_router

app = FastAPI()
router = fastapi.APIRouter()

@router.get('/')
async def get_app_info(_request: Request):
    return {
        'appName': 'tuVino',
        'version': '0.0.1',
    }

router.include_router(router=users_router)
app.include_router(router=router)
