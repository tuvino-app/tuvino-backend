import fastapi
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from api.routes.users import router as users_router

from api.endpoints import router as api_endpoint_router
from config.manager import settings

load_dotenv()

app = FastAPI()
router = fastapi.APIRouter()

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def initialize_app() -> fastapi.FastAPI:
    fastapi_app = fastapi.FastAPI(**settings.set_backend_app_attributes)

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    fastapi_app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    return fastapi_app

@router.get('/')
async def get_app_info(_request: Request):
    return {
        'appName': 'tuVino',
        'version': '0.0.1',
    }

initialize_log(logging.INFO)
router.include_router(router=users_router)
tuvino_backend: fastapi.FastAPI = initialize_app()
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
