#!/usr/bin/python3
"""defines a class Statement"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy import Integer, Table
from sqlalchemy.orm import relationship


class Statement(BaseModel, Base):
    """Model for member statements."""
    __tablename__ = 'statements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_name = Column(String(255), nullable=False)
    outstanding_fee = Column(Float, nullable=False, default=0.0)
    issuances = relationship('Issuance', secondary='issuance_statement',
                            back_populates='statements')


issuance_statement = Table(
    'issuance_statement',
    Base.metadata,
    Column('issuance_id', Integer, ForeignKey('issuances.id')),
    Column('statement_id', Integer, ForeignKey('statements.id'))
    )
