from datetime import datetime
import unittest
import models
from models.statement import Statement
from models.base_model import BaseModel
from sqlalchemy.orm import relationship

class TestStatement(unittest.TestCase):
    """Test the Statement class"""

    def test_is_subclass(self):
        """Test that Statement is a subclass of BaseModel"""
        statement = Statement()
        self.assertIsInstance(statement, BaseModel)
        self.assertTrue(hasattr(statement, "id"))
        self.assertTrue(hasattr(statement, "created_at"))
        self.assertTrue(hasattr(statement, "updated_at"))

    def test_attributes(self):
        """Test that Statement has the required attributes"""
        statement = Statement()
        self.assertTrue(hasattr(statement, "member_name"))
        self.assertTrue(hasattr(statement, "outstanding_fee"))

    def test_constructor(self):
        """Test the constructor"""
        statement = Statement(member_name="John Doe", outstanding_fee=0.0)
        self.assertIsNotNone(statement)
        self.assertEqual(statement.member_name, "John Doe")
        self.assertEqual(statement.outstanding_fee, 0.0)

    def test_module_docstring(self):
        """Test for the module docstring"""
        self.assertIsNot(Statement.__doc__, None,
                         "Statement module needs a docstring")
        self.assertTrue(len(Statement.__doc__) >= 1,
                        "Statement module needs a docstring")

    def test_class_docstring(self):
        """Test for the Statement class docstring"""
        self.assertIsNot(Statement.__doc__, None,
                         "Statement class needs a docstring")
        self.assertTrue(len(Statement.__doc__) >= 1,
                        "Statement class needs a docstring")
