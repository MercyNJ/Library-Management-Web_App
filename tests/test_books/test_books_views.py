#!/usr/bin/python3
"""
Contains tests for the books routes
"""

import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from models.books import Books
from models import storage
from flask_login import current_user

class TestBooksViews(unittest.TestCase):
    """Tests for Books Views"""

    def setUp(self):
        """Set up the test environment"""
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down the test environment"""
        pass

    @patch('models.storage.get')
    @patch('flask_login.utils._get_user')
    def test_add_book_form(self, mock_get_user, mock_get):
        """Test add_book_form route"""
        mock_get_user.return_value = MagicMock(is_authenticated=True)
        with self.app.app_context():
            response = self.client.post('/add_book_form', data={'book_name': 'New Book', 'book_author': 'New Author', 'book_original_stock': 10, 'book_current_stock': 10})
            self.assertEqual(response.status_code, 302)

    @patch('models.storage.get')
    @patch('flask_login.utils._get_user')
    def test_update_book_form(self, mock_get_user, mock_get):
        """Test update_book_form route"""
        mock_get_user.return_value = MagicMock(is_authenticated=True)
        with self.app.app_context():
            mock_book = MagicMock(spec=Books)
            mock_book.id = 1
            mock_book.name = 'Updated Book'
            mock_book.author = 'Updated Author'
            mock_book.original_stock = 20
            mock_book.current_stock = 15
            storage.get = MagicMock(return_value=mock_book)
            response = self.client.post('/update_book_form/1', data={'book_name': 'Updated Book', 'book_author': 'Updated Author', 'book_original_stock': 20, 'book_current_stock': 15})
            self.assertEqual(response.status_code, 302)

    @patch('models.storage.get')
    @patch('flask_login.utils._get_user')
    def test_delete_book(self, mock_get_user, mock_get):
        """Test delete_book route"""
        mock_get_user.return_value = MagicMock(is_authenticated=True)
        with self.app.app_context():
            mock_book = MagicMock(spec=Books)
            mock_book.id = 1
            storage.get = MagicMock(return_value=mock_book)
            response = self.client.get('/delete_book/1')
            self.assertEqual(response.status_code, 200)
