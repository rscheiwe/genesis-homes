from project.properties import models
from project.users.models import User
from sqlalchemy.orm import Session


def get_property(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()


def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Property).offset(skip).limit(limit).all()


def get_property_by_user_id(db: Session, user_id: int):
    return db.query(models.Property).filter(models.Property.owner_id == user_id).first()

# def get_user_property(db: Session, )