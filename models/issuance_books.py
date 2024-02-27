#!/usr/bin/python3
"""defines an association model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


class IssuanceBooks(BaseModel, Base):
    """Model for Issuance & books association"""
    __tablename__ = 'issuance_books'

    id = Column(Integer, primary_key=True)
    issuance_id = Column(Integer, ForeignKey('issuances.id'), nullable=False)
    books_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    associated_book = relationship('Books')

    def __init__(self, *args, **kwargs):
        """Initialization method"""
        super().__init__(*args, **kwargs)
