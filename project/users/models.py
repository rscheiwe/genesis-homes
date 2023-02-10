from datetime import datetime
from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from project.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)

    user_roles = relationship("UserRole", back_populates="user")
    properties = relationship('Property', back_populates='owner')

    def __init__(self, username, email, hashed_password, is_active):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String, index=True)
    created = Column(DateTime, default=func.now())

    user_roles = relationship("UserRole", back_populates="role")

    def __init__(self, role_name, created=None):
        self.role_name = role_name
        self.created_at = created if created is not None else datetime.now()


class UserRole(Base):
    __tablename__ = "userroles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    role_name = Column(String)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")





