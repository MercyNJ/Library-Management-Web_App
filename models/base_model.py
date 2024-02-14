#!/usr/bin/python3
"""Defines a class basemodel"""
from datetime import datetime
import models
import uuid
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%H:%M"
Base = declarative_base()


class BaseModel:
    """define Basemodel"""
    id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now()
        else:
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """return string rep"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """saves the instance created"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """return a dictionary representation"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict['__class__'] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict['_sa_instance_state']
        return new_dict

    def delete(self):
        """deletes and instance"""
        models.storage.delete(self)
