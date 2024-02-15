#!/usr/bin/python3
"""defines a class member"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Members(BaseModel, Base):
    """define a member model"""
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    contact = Column(String(13), nullable=False)
    total_fee_due = Column(Float, nullable=False, default=0.0)
    issuances = relationship('Issuance', backref='members',
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes the members"""
        super().__init__(*args, **kwargs)

    @hybrid_property
    def total_borrowed_books(self):
        """Calculates total borrowed books for the member"""
        total_books = sum(len(issuance.books) for issuance in self.issuances)
        return total_books

    @hybrid_property
    def total_fee_due(self):
        """Calculate the total fee due for the member."""
        total_fee_due = sum(issuance.total_fee for issuance in self.issuances)
        return min(total_fee_due, 500)

    def can_make_issuance(self):
    """Check if a new issuance can be made to the member."""
    return self.total_fee_due < 500

