from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs import get_environment
from app.routers import health_router, user_router

_env = get_environment()


def create_app():
    app = FastAPI(title=_env.APPLICATION_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(user_router)

    return app
