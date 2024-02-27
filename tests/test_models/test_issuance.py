import unittest
import pep8
from datetime import datetime
from models import books
from models.members import Members
from models.statement import Statement
from models.issuance import Issuance
from models.base_model import BaseModel


Books = books.Books


class TestIssuanceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Issuance class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.issuance_f = [
            x for x, _ in Issuance.__dict__.items() if callable(getattr(Issuance, x))]

    def test_pep8_conformance_issuance(self):
        """Test that models/issuance.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/issuance.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings) in models/issuance.py.")

    def test_pep8_conformance_test_issuance(self):
        """Test that tests/test_models/test_issuance.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_issuance.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings) in tests/test_models/test_issuance.py.")


    def test_issuance_class_docstring(self):
        """Test for the Issuance class docstring"""
        self.assertIsNot(Issuance.__doc__, None,
                         "Issuance class needs a docstring")
        self.assertTrue(len(Issuance.__doc__) >= 1,
                        "Issuance class needs a docstring")

    def test_issuance_func_docstrings(self):
        """Test for the presence of docstrings in Issuance methods"""
        for func in self.issuance_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestIssuance(unittest.TestCase):
    """Test the Issuance class"""
    def test_is_subclass(self):
        """Test that Issuance is a subclass of BaseModel"""
        issuance = Issuance(member_id=1, due_date=datetime.now().date(),
                            books_borrowed="books", contact_number="12345", total_fee=10.0)
        self.assertIsInstance(issuance, BaseModel)
        self.assertTrue(hasattr(issuance, "id"))
        self.assertTrue(hasattr(issuance, "created_at"))
        self.assertTrue(hasattr(issuance, "updated_at"))

    def test_attributes(self):
        """Test that Issuance has the required attributes"""
        issuance = Issuance(member_id=1, due_date=datetime.now().date(),
                            books_borrowed="books", contact_number="12345", total_fee=10.0)
        self.assertTrue(hasattr(issuance, "books_borrowed"))
        self.assertTrue(hasattr(issuance, "contact_number"))
        self.assertTrue(hasattr(issuance, "return_status"))
        self.assertTrue(hasattr(issuance, "total_fee"))
        self.assertTrue(hasattr(issuance, "due_date"))
        self.assertTrue(hasattr(issuance, "member_id"))


    def test_calculate_total_fee(self):
        """Test calculate_total_fee method"""
        issuance = Issuance(member_id=1, due_date=datetime.now().date(),
                            books_borrowed="books", contact_number="12345", total_fee=10.0)
        issuance.calculate_total_fee()
        self.assertEqual(issuance.total_fee, 0.0)

        issuance.return_status = "overdue"
        issuance.books = [Books(), Books()]
        issuance.calculate_total_fee()
        self.assertEqual(issuance.total_fee, 100.0)

