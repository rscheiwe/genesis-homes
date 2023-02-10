from fastapi import APIRouter


properties_router = APIRouter(
    prefix="/genesis-properties",
    tags=["Properties"],
)

from . import views, models # noqa