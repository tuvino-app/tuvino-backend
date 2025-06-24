import fastapi
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form

from routes.users import router as users_router

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

@router.get('/')
async def get_app_info(_request: Request):
    return {
        'appName': 'tuVino',
        'version': '0.0.1',
    }

initialize_log(logging.INFO)
router.include_router(router=users_router)
app.include_router(router=router)

