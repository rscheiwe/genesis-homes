from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from project.database import Base


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_address = Column(String, unique=True, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='properties')

    def __init__(self, property_address, owner_id):
        self.property_address = property_address
        self.owner_id = owner_id