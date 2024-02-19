#!/usr/bin/python3
"""defines a class Books"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Books(BaseModel, Base):
    """Model for books records."""
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    original_stock = Column(Integer, nullable=False, default=0)
    current_stock = Column(Integer, nullable=False, default=0)
    author = Column(String(255), nullable=False)
    issuances = relationship('Issuance',
                            secondary='issuance_books',
                            back_populates='books', viewonly=True)


    def reduce_stock(self, quantity):
        """Updates the quantity in stock"""
        if self.current_stock >= quantity:
            self.current_stock -= quantity
            return True
        else:
            return False
