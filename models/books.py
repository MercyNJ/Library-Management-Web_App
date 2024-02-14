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
    quantity_in_stock = Column(Float, default=0)
    issuances = relationship('Issuance',
                            secondary='issuance_books',
                            back_populates='books')


    def reduce_stock(self, quantity):
        """Updates the quantity in stock"""
        if self.quantity_in_stock >= quantity:
            self.quantity_in_stock -= quantity
            return True
        else:
            return False
