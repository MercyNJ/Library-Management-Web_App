#!/usr/bin/python3
"""
Contains tests for the console
"""

import unittest
import pep8
import console

LIBCommand = console.LIBCommand

class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_LIBCommand_class_docstring(self):
        """Test for the LIBCommand class docstring"""
        self.assertIsNot(LIBCommand.__doc__, None,
                         "LIBCommand class needs a docstring")
        self.assertTrue(len(LIBCommand.__doc__) >= 1,
                        "LIBCommand class needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(LIBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(LIBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")
