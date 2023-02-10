from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from project.database import db_context
from fastapi import Depends, HTTPException, status
from project.users.schemas import UserBase, TokenData, UserToken
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Union, List
from project.users.models import User

from project.users import schemas
from project.database import get_db_session

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "55a72aafb96da40d502a6a2aef90836125a5b85a063c96921b28e68d8b2e90b3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_roles_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user.user_roles[0].role_name

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_user(username: str):
    with db_context() as session:
        user = session.query(User).filter(User.username == username).first()
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    with db_context() as session:
        user_login = session.query(User).filter(User.username == username).first()

        if user_login:
            if verify_password(password, user_login.__dict__['hashed_password']):
                return user_login
        return False


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user["is_active"] == 0:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: schemas.UserToken = Depends(get_current_user), db: Session = Depends(get_db_session)):

        role = get_roles_by_username(db, user.username)

        if role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail=f"Operation not permitted: Your role of {role} does not have sufficient permissions.")