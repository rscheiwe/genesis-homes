from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from project.database import get_db_session
from project.users import crud, schemas
from project.security import get_current_user, RoleChecker
from . import users_router


@users_router.get(
    '/users',
    response_model=List[schemas.UserBase],
    dependencies=[Depends(RoleChecker(["ADMIN"]))]
)
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    """
    Retrieve all users.

    NOTE: Admin-level only
    """
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@users_router.get("/current-user", response_model=schemas.UserBase)
async def read_user_self(
        current_user: schemas.UserBase = Depends(get_current_user),
        db: Session = Depends(get_db_session)
):
    """
    Retrieve currently authenticated user data.

    NOTE: Must be authenticated.
    """
    return crud.get_user_by_email(db, email=current_user.email)


@users_router.get(
    '/users/{user_id}',
    response_model=schemas.UserBase,
    dependencies=[Depends(RoleChecker(["ADMIN"]))]
)
def read_user_by_id(user_id: int, db: Session = Depends(get_db_session)):
    """
    Retrieve user and user properties by user ID.

    NOTE: Admin-level only
    """
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user
