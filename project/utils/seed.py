import os
from datetime import datetime
import pathlib
from contextlib import contextmanager
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_inc = 1

BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent


def _get_str_inc():
    global _inc
    s = str(_inc)
    _inc = _inc + 1
    return s


def _reset_inc():
    global _inc
    _inc = 1


DATABASE_URL: str = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///./sql_app.db"
)

DATABASE_CONNECT_DICT: dict = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=DATABASE_CONNECT_DICT,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


db_context = contextmanager(get_db_session)


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


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_address = Column(String, unique=True, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='properties')

    def __init__(self, property_address, owner_id):
        self.property_address = property_address
        self.owner_id = owner_id


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

    def __init__(self, user_id, role_id, role_name):
        self.user_id = user_id
        self.role_id = role_id
        self.role_name = role_name


session = SessionLocal()

with db_context() as session:

    session.query(User).delete()
    session.query(Property).delete()
    session.query(Role).delete()
    session.query(UserRole).delete()

    role_admin = Role(
        role_name="ADMIN",
    )
    role_user = Role(
        role_name="USER"
    )

    session.add_all([role_admin, role_user])
    _reset_inc()

    admin = User(
        username="admin",
        email="admin@genesis.demo",
        hashed_password="$2b$12$E7tz4yNWkmZXwXNHpVUc2.tEfZuSaafxh0EKcY53BlOcZ69IKd7vq",
        is_active=1
    )
    alice = User(
        username="alice",
        email="alice@genesis.demo",
        hashed_password="$2b$12$63zmeHZAUSY.jkFgZqsWVuMqF7mmMOtQ.9oz2DPWz5i/LsYv7NUcS",
        is_active=1
    )
    john = User(
        username="john",
        email="john@genesis.demo",
        hashed_password="$2b$12$06nNwjvnZj7CT8xtp2eevObmqp0l2ngOFEWF1Aj8z/MRrbLvtT.ze",
        is_active=1
    )
    sarah = User(
        username="sarah",
        email="sarah@genesis.demo",
        hashed_password="$2b$12$.rgMEulqsgZLNdWA7JVFVepy0iqQOuVWtmcw9O3WM/.6UoFTYJqiy",
        is_active=1
    )
    geri = User(
        username="geri",
        email="geri@genesis.demo",
        hashed_password="$2b$12$8U.OSDbx00R/DMj6yw8HDOIz0qfV5TOoVeEbVfkbSl3bLMAiBvujG",
        is_active=0
    )
    session.add_all([admin, alice, john, sarah, geri])
    _reset_inc()

    prop_1 = Property(
        property_address="4974 Johanna Forks, Shainafort, CT 572476",
        owner_id=2
    )

    prop_2 = Property(
        property_address="871 Predovic Meadow, Port Emersonside, SD 41277",
        owner_id=3
    )

    prop_3 = Property(
        property_address="4553 Haley Stream Apt. 502, Lakinstad, MT 41214",
        owner_id=4
    )

    prop_4 = Property(
        property_address="375 Buckridge Light Apt. 154, Karlimouth, IA 37545-4100",
        owner_id=5
    )

    session.add_all([prop_1, prop_2, prop_3, prop_4])

    admin_user_role = UserRole(
        user_id=1,
        role_id=1,
        role_name="ADMIN"
    )

    alice_user_role = UserRole(
        user_id=2,
        role_id=2,
        role_name="USER"

    )

    john_user_role = UserRole(
        user_id=3,
        role_id=2,
        role_name="USER"

    )

    sarah_user_role = UserRole(
        user_id=4,
        role_id=2,
        role_name="USER"

    )

    geri_user_role = UserRole(
        user_id=5,
        role_id=2,
        role_name="USER"

    )

    session.add_all([
        admin_user_role,
        alice_user_role,
        john_user_role,
        sarah_user_role,
        geri_user_role
    ])


    try:
        session.commit()
    except BaseException as e:
        session.rollback()
        raise e
    finally:
        session.close()

