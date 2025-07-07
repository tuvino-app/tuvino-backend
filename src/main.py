import fastapi
import logging
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from src.api.endpoints import router as api_endpoint_router
from src.api.endpoints import default_router
from src.config.manager import settings
from src.config.events import execute_backend_server_event_handler, terminate_backend_server_event_handler

load_dotenv()

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

    @fastapi_app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    @fastapi_app.exception_handler(Exception)
    async def internal_server_error_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"error": exc.detail},
        )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    fastapi_app.add_event_handler(
        "startup",
        lambda: execute_backend_server_event_handler(backend_app=app),
    )
    fastapi_app.add_event_handler(
        "shutdown",
        lambda: terminate_backend_server_event_handler(backend_app=app),
    )

    fastapi_app.include_router(router=default_router, prefix='')
    fastapi_app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    return fastapi_app

initialize_log(logging.INFO)
app: FastAPI = initialize_app()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
