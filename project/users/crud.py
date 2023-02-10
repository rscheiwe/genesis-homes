from typing import List
from project.properties.schemas import PropertyCreate
from project.users import models
from project.database import get_db_session
from project.users import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from project.security import get_password_hash, get_current_user


# class RoleChecker:
#     def __init__(self, allowed_roles: List):
#         self.allowed_roles = allowed_roles
#
#     def __call__(self, user: schemas.UserToken = Depends(get_current_user), db: Session = Depends(get_db_session)):
#
#         role = get_roles_by_username(db, user.username)
#
#         if role not in self.allowed_roles:
#             raise HTTPException(status_code=403, detail=f"Operation not permitted: Your role of {role} does not have sufficient permissions.")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_roles_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    # return user.user_roles
    return user.user_roles[0].role_name


def get_role_names(db: Session, roles: List[models.UserRole]):
    names = list()
    for role in roles:
        role_item = db.query(models.Role).filter(models.Role.id == role.id).first()
        names.append(role_item.role_name)

    return names


def create_user(db: Session, user: schemas.UserCreate):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        return False

    new_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=new_password,
        is_active=1
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def create_user_property(db: Session, property: PropertyCreate, user_id: int):
    db_home_work = PropertyCreate(**property.dict(), owner_id=user_id)
    db.add(db_home_work)
    db.commit()
    db.refresh(db_home_work)

    return db_home_work
