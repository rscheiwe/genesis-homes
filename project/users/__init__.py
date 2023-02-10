from fastapi import APIRouter


users_router = APIRouter(
    prefix="/genesis-users",
    tags=["Users"],
)

from . import views, models # noqa
