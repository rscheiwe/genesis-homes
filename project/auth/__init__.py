from fastapi import APIRouter


auth_router = APIRouter(
    tags=["Auth"],
)

from . import views # noqa