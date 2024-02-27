#!/usr/bin/python3
"""
Module for the database class.
"""

import models
from models.base_model import BaseModel, Base
from models.books import Books
from models.members import Members
from models.issuance import Issuance
from models.statement import Statement
from models.user import User
from models.issuance_books import IssuanceBooks
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

classes = {"Members": Members, "Books": Books, "Issuance": Issuance,
        "Statement": Statement, "User": User, "IssuanceBooks": IssuanceBooks}


class DBStorage:
    """Sets up class interaction with MySql Database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization method"""
        USER = getenv('LIB_MYSQL_USER')
        PWD = getenv('LIB_MYSQL_PWD')
        HOST = getenv('LIB_MYSQL_HOST')
        DB = getenv('LIB_MYSQL_DB')
        ENV = getenv('LIB_ENV')

        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_recycle': 280,
            'pool_pre_ping': True
        }

        self.__engine = create_engine(
            f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}',
            **SQLALCHEMY_ENGINE_OPTIONS)

        if ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrive all objects of a class"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
