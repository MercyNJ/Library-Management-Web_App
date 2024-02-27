#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models import storage
from models.base_model import BaseModel
from models.books import Books
from models.members import Members
from models.issuance import Issuance
from models.statement import Statement
from models.user import User
from models.issuance_books import IssuanceBooks
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage

classes = {"Books": Books, "Members": Members, "Issuance": Issuance,
           "Statement": Statement, "User": User, "IssuanceBooks": IssuanceBooks}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in [func for func in dir(DBStorage)
                     if callable(getattr(DBStorage, func))]:
            self.assertIsNot(func.__doc__, None,
                             "{:s} method needs a docstring".format(func))
            self.assertTrue(len(func.__doc__) >= 1,
                            "{:s} method needs a docstring".format(func))

class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    def setUp(self):
        """Set up the test environment"""
        self.storage = storage

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test that new adds an object to the database"""
        prev_count = len(self.storage.all())
        new_model = BaseModel()
        new_model.save()
        self.assertTrue(len(self.storage.all()) == prev_count + 1)

    def test_save(self):
        """Test that save properly saves objects to the database"""
        new_model = BaseModel()
        new_model.save()
        new_model_copy = self.storage.all()[new_model.__class__.__name__ + "." + new_model.id]
        self.assertEqual(new_model, new_model_copy)

    def test_delete(self):
        """Test that delete removes an object from the database"""
        new_model = BaseModel()
        new_model.save()
        prev_count = len(self.storage.all())
        self.storage.delete(new_model)
        self.assertTrue(len(self.storage.all()) == prev_count - 1)

    def test_reload(self):
        """Test that reload reloads the storage correctly"""
        prev_count = len(self.storage.all())
        new_model = BaseModel()
        new_model.save()
        self.assertTrue(len(self.storage.all()) == prev_count + 1)
        self.storage.reload()
        self.assertTrue(len(self.storage.all()) == prev_count)

    def test_close(self):
        """Test that close closes the session"""
        self.storage.close()
        self.assertIsNone(self.storage._DBStorage__session)

    def test_get(self):
        """Test that get returns correct object by id"""
        new_model = BaseModel()
        new_model.save()
        self.assertEqual(new_model, self.storage.get(BaseModel, new_model.id))

    def test_count(self):
        """Test that count returns correct number of items"""
        prev_count = len(self.storage.all())
        new_model = BaseModel()
        new_model.save()
        self.assertEqual(self.storage.count(), prev_count + 1)

if __name__ == "__main__":
    unittest.main()

