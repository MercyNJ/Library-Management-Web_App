#!/usr/bin/python3
"""defines a class member"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship


class Members(BaseModel, Base):
    """define a member model"""
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False)
    contact = Column(String(13), nullable=False)
    total_fee_due = Column(Float, nullable=False, default=0.0)
    issuances = relationship('Issuance', backref='members',
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes the members"""
        super().__init__(*args, **kwargs)
