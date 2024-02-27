import unittest
from models.members import Members
from models.issuance import Issuance
from models.base_model import BaseModel
import inspect
import pep8

class TestMembers(unittest.TestCase):
    """Test the Members class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.members_f = []


    def test_is_subclass(self):
        """Test that Members is a subclass of BaseModel"""
        member = Members()
        self.assertIsInstance(member, BaseModel)
        self.assertTrue(hasattr(member, "id"))
        self.assertTrue(hasattr(member, "created_at"))
        self.assertTrue(hasattr(member, "updated_at"))

    def test_attributes(self):
        """Test that Members has the required attributes"""
        member = Members()
        self.assertTrue(hasattr(member, "name"))
        self.assertTrue(hasattr(member, "email"))
        self.assertTrue(hasattr(member, "contact"))
        self.assertTrue(hasattr(member, "total_fee_due"))

    def test_relationship(self):
        """Test the relationship with Issuance"""
        member = Members()
        self.assertTrue(hasattr(member, "issuances"))

    def test_constructor(self):
        """Test the constructor"""
        member = Members()
        self.assertIsNotNone(member)

    def test_module_docstring(self):
        """Test for the module docstring"""
        self.assertIsNot(Members.__doc__, None)
        self.assertTrue(len(Members.__doc__) >= 1)

    def test_class_docstring(self):
        """Test for the Members class docstring"""
        self.assertIsNot(Members.__doc__, None)
        self.assertTrue(len(Members.__doc__) >= 1)

    def test_function_docstrings(self):
        """Test for the presence of docstrings in Members methods"""
        for func in self.members_f:
            self.assertIsNot(func[1].__doc__, None)
            self.assertTrue(len(func[1].__doc__) >= 1)

    def test_pep8_conformance(self):
        """Test that models/members.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/members.py'])
        self.assertEqual(result.total_errors, 0)

    def test_total_borrowed_books(self):
        """Test total_borrowed_books hybrid property"""
        member = Members()
        # Create Issuance objects representing borrowed books
        issuance1 = Issuance(member_id=member.id, due_date="2024-02-27", books_borrowed="Book1", contact_number="123456789", total_fee=0)
        issuance2 = Issuance(member_id=member.id, due_date="2024-02-28", books_borrowed="Book2", contact_number="123456789", total_fee=0)

    # Add Issuance objects to the member's issuances relationship
        member.issuances.append(issuance1)
        member.issuances.append(issuance2)

    # Test total_borrowed_books property
        self.assertEqual(member.total_borrowed_books, 2)

    def test_total_fee_due(self):
        """Test total_fee_due hybrid property"""
        member = Members()
    # Create Issuance objects representing borrowed books with fees
        issuance1 = Issuance(member_id=member.id, due_date="2024-02-27", books_borrowed="Book1", contact_number="123456789", total_fee=50)
        issuance2 = Issuance(member_id=member.id, due_date="2024-02-28", books_borrowed="Book2", contact_number="123456789", total_fee=100)

    # Add Issuance objects to the member's issuances relationship
        member.issuances.append(issuance1)
        member.issuances.append(issuance2)

    # Test total_fee_due propertydd
        self.assertEqual(member.total_fee_due, 150)
