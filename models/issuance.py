#!/usr/bin/python3
"""create issuance model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, Date
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from models.issuance_books import IssuanceBooks
from datetime import datetime


issuance_book = Table(
    'issuance_book',
    Base.metadata,
    Column('issuance_id', Integer, ForeignKey('issuances.id')),
    Column('books_id', Integer, ForeignKey('books.id'))
)


class Issuance(BaseModel, Base):
    """Model for issuance records."""
    __tablename__ = 'issuances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    books_borrowed = Column(String(255), nullable=False,
                              default="to be determined")
    contact_number = Column(String(20), nullable=False)
    return_status = Column(String(20), nullable=False, default="borrowed")
    total_fee = Column(Float, nullable=False, default=0.0)
    due_date = Column(Date, nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    books = relationship('Books', secondary=issuance_book,
                            back_populates='issuances')
    statements = relationship('Statement', secondary='issuance_statement',
                              back_populates='issuances')
    issued_books = relationship('IssuanceBooks', back_populates='issuance', cascade="all, delete, delete-orphan")


    def __init__(self, member_id, due_date,
                 books_borrowed, contact_number, total_fee,
                 books=None):
        """Initializes the issuance"""
        super().__init__()
        self.member_id = member_id
        self.due_date = due_date
        self.books_borrowed = books_borrowed
        self.contact_number = contact_number
        self.books = books or []
        self.total_fee = total_fee

    def issuance_status(self):
        """Update the status of the issuance based on due date."""
        if self.return_status != "returned":
            if self.due_date < datetime.now().date():
                self.return_status = "overdue"
                self.calculate_total_fee()
            else:
                self.return_status = "borrowed"

    def calculate_total_fee(self):
        """Calculate the total fee for the issuance."""
        if self.return_status == "overdue":
            total_books = len(self.books)
            self.total_fee = min(total_books * 50, 500)
        else:
            self.total_fee = 0.0

    
