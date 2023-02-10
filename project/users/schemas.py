from typing import List, Union
from pydantic import BaseModel

from project.properties.schemas import Property


class UserRoleBase(BaseModel):
    id: int


class UserRole(UserRoleBase):
    role_id: int
    role_name: str

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    role_name: str


class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    is_active: bool
    user_roles: List[UserRole] = []
    properties: List[Property] = []

    class Config:
        orm_mode = True


class UserProperty(BaseModel):
    username: str
    properties: List[Property] = []

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserToken(BaseModel):
    username: str
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str
    data: dict


class TokenData(BaseModel):
    username: Union[str, None] = None
