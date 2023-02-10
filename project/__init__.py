from fastapi.middleware.cors import CORSMiddleware
# from project.celery_utils import create_celery
# from project.users import models
from .database import engine

from fastapi import FastAPI

# models.Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        # Usually REACT
        "http://localhost:3000",
        # Usually Python
        "http://localhost:8010",
        # Redundant
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.celery_app = create_celery()
    from project.users import users_router
    app.include_router(users_router)

    from project.properties import properties_router
    app.include_router(properties_router)

    from project.auth import auth_router
    app.include_router(auth_router)


    @app.get("/")
    async def root():
        return {
            "name": "Genesis Homes - Feature Detection API -- Sewage System",
            "version": "1.0.0",
        }

    return app
