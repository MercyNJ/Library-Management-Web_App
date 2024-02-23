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
                            secondary='issuance_book',
                            back_populates='books')


    def reduce_stock(self, quantity):
        """Updates the quantity in stock"""
        if self.current_stock >= quantity:
            self.current_stock -= quantity
            return True
        else:
            return False

    def update_current_stock(self):
        """Update the current stock of the book."""
        total_issued_quantity = sum(
                issuance.quantity for issuance in self.issuances)
        total_returned_quantity = sum(
                issuance.quantity for issuance in self.issuances \
                        if issuance.return_status == "returned")
        self.current_stock = \
                (self.original_stock - total_issued_quantity) + total_returned_quantity
        if self.current_stock < 0:
            self.current_stock = 0

        self.save()
