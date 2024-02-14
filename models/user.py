#!/usr/bin/python3
"""defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

max_length = 20


class User(UserMixin, BaseModel, Base):
    """define a class and it table"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(500), nullable=False)
    username = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def set_password(self, password):
        """sets the password to hashed"""
        hashed_password = generate_password_hash(password)
        self.password = hashed_password

    def check_password(self, password):
        """check the password"""
        return check_password_hash(self.password, password)
