import unittest
import inspect
from models.user import User
from models.base_model import BaseModel

class TestUser(unittest.TestCase):
    """Test the User class"""

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(User.__doc__, None, "user.py needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1, "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNot(User.__doc__, None, "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1, "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            if func[0] != 'get_id':
                self.assertIsNot(func[1].__doc__, None, f"{func[0]} method needs a docstring")
