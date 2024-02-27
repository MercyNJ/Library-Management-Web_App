import unittest
from models.issuance_books import IssuanceBooks
from models.base_model import BaseModel
import inspect
import pep8

class TestIssuanceBooks(unittest.TestCase):
    """Test the IssuanceBooks class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.issuance_books_f = inspect.getmembers(IssuanceBooks, inspect.isfunction)

    def test_is_subclass(self):
        """Test that IssuanceBooks is a subclass of BaseModel"""
        issuance_book = IssuanceBooks()
        self.assertIsInstance(issuance_book, BaseModel)
        self.assertTrue(hasattr(issuance_book, "id"))
        self.assertTrue(hasattr(issuance_book, "created_at"))
        self.assertTrue(hasattr(issuance_book, "updated_at"))

    def test_attributes(self):
        """Test that IssuanceBooks has the required attributes"""
        issuance_book = IssuanceBooks()
        self.assertTrue(hasattr(issuance_book, "issuance_id"))
        self.assertTrue(hasattr(issuance_book, "books_id"))
        self.assertTrue(hasattr(issuance_book, "quantity"))

    def test_relationship(self):
        """Test the relationship with Books"""
        issuance_book = IssuanceBooks()
        self.assertTrue(hasattr(issuance_book, "associated_book"))

    def test_constructor(self):
        """Test the constructor"""
        issuance_book = IssuanceBooks()
        self.assertIsNotNone(issuance_book)

    def test_module_docstring(self):
        """Test for the module docstring"""
        self.assertIsNot(IssuanceBooks.__doc__, None,
                         "IssuanceBooks module needs a docstring")
        self.assertTrue(len(IssuanceBooks.__doc__) >= 1,
                        "IssuanceBooks module needs a docstring")

    def test_class_docstring(self):
        """Test for the IssuanceBooks class docstring"""
        self.assertIsNot(IssuanceBooks.__doc__, None,
                         "IssuanceBooks class needs a docstring")
        self.assertTrue(len(IssuanceBooks.__doc__) >= 1,
                        "IssuanceBooks class needs a docstring")

    def test_function_docstrings(self):
        """Test for the presence of docstrings in IssuanceBooks methods"""
        for func in self.issuance_books_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_pep8_conformance(self):
        """Test that models/issuance_books.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/issuance_books.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
