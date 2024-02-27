from datetime import datetime
import inspect
import models
from models import books
from models.members import Members
from models.issuance import Issuance
from models.base_model import BaseModel
import pep8
import unittest

Books = books.Books


class TestBooksDocs(unittest.TestCase):
    """Tests to check the documentation and style of Books class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.books_f = inspect.getmembers(Books, inspect.isfunction)

    def test_pep8_conformance_books(self):
        """Test that models/books.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/books.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_books(self):
        """Test that tests/test_models/test_books.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_books.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_books_module_docstring(self):
        """Test for the books.py module docstring"""
        self.assertIsNot(books.__doc__, None,
                         "books.py needs a docstring")
        self.assertTrue(len(books.__doc__) >= 1,
                        "books.py needs a docstring")

    def test_books_class_docstring(self):
        """Test for the Books class docstring"""
        self.assertIsNot(Books.__doc__, None,
                         "Books class needs a docstring")
        self.assertTrue(len(Books.__doc__) >= 1,
                        "Books class needs a docstring")

    def test_books_func_docstrings(self):
        """Test for the presence of docstrings in Books methods"""
        for func in self.books_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestBooks(unittest.TestCase):
    """Test the Books class"""
    def test_is_subclass(self):
        """Test that Books is a subclass of BaseModel"""
        book = Books()
        self.assertIsInstance(book, BaseModel)
        self.assertTrue(hasattr(book, "id"))
        self.assertTrue(hasattr(book, "created_at"))
        self.assertTrue(hasattr(book, "updated_at"))

    def test_attributes(self):
        """Test that Books has the required attributes"""
        book = Books()
        self.assertTrue(hasattr(book, "name"))
        self.assertTrue(hasattr(book, "original_stock"))
        self.assertTrue(hasattr(book, "current_stock"))
        self.assertTrue(hasattr(book, "author"))

    def test_reduce_stock(self):
        """Test reduce_stock method"""
        book = Books(original_stock=10, current_stock=10)
        self.assertTrue(book.reduce_stock(5))
        self.assertEqual(book.current_stock, 5)
        self.assertFalse(book.reduce_stock(10))
