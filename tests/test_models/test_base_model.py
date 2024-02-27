from datetime import datetime
import models
import pep8 as pycodestyle
import time
import unittest
import inspect
from unittest import mock
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.base_funcs = [(name, member) for name, member in inspect.getmembers(BaseModel, inspect.isfunction)]

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/base_model.py', 'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None, "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1, "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for name, func in self.base_funcs:
            with self.subTest(function=name):
                self.assertIsNot(func.__doc__, None, f"{name} method needs a docstring")
                self.assertTrue(len(func.__doc__) > 1, f"{name} method needs a docstring")


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_datetime_attributes(self):
        """Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value."""
        tic = datetime.utcnow()
        inst1 = BaseModel()
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.utcnow()
        inst2 = BaseModel()
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_save(self):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        with mock.patch('models.storage') as mock_storage:
            inst = BaseModel()
            old_created_at = inst.created_at
            old_updated_at = inst.updated_at
            inst.save()
            new_created_at = inst.created_at
            new_updated_at = inst.updated_at
            self.assertNotEqual(old_updated_at, new_updated_at)
            self.assertEqual(old_created_at, new_created_at)
            self.assertTrue(mock_storage.new.called)
            self.assertTrue(mock_storage.save.called)


    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)

    def test_str(self):
        """test that the str method has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))


if __name__ == '__main__':
    unittest.main()

