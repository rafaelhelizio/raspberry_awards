import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs import get_environment
from app.routers import movies
from app.use_cases.movies import upload_csv

_env = get_environment()

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(base_dir, "db", "data", "movielist.csv")

def create_app():
    app = FastAPI(title=_env.APPLICATION_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    file = open(csv_file)

    upload_csv(file.read())
    app.include_router(movies) 

    return app
