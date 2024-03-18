#!/usr/bin/python3
"""
Contains tests for the members routes
"""

import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from models.members import Members
from models import storage
from flask_login import current_user

class TestMembersViews(unittest.TestCase):
    """Tests for Members Views"""

    def setUp(self):
        """Set up the test environment"""
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down the test environment"""
        pass

    @patch('models.storage.all')
    def test_view_members(self, mock_all):
        """Test view_members route"""
        mock_member = MagicMock(spec=Members)
        mock_all.return_value = {1: mock_member, 2: mock_member}
        with self.app.app_context():
            response = self.client.get('/members')
            self.assertEqual(response.status_code, 200)

    @patch('models.storage.all')
    def test_search_members(self, mock_all):
        """Test search_members route"""
        mock_member1 = MagicMock(spec=Members)
        mock_member2 = MagicMock(spec=Members)
        mock_all.return_value = {1: mock_member1, 2: mock_member2}
        with self.app.app_context():
            response = self.client.post('/search_members', data={'search': 'test'})
            self.assertEqual(response.status_code, 200)

    @patch('models.storage.save')
    @patch('models.storage.get')
    def test_add_member_form(self, mock_get, mock_save):
        """Test add_member_form route"""
        mock_get.return_value = MagicMock()
        with self.app.app_context():
            response = self.client.post('/add_member_form', data={'member_name': 'Test Name', 'member_email': 'test@example.com', 'member_contact': '1234567890'})
            self.assertEqual(response.status_code, 302)

    @patch('models.storage.get')
    def test_update_member_form(self, mock_get):
        """Test update_member_form route"""
        mock_get.return_value = MagicMock(spec=Members)
        with self.app.app_context():
            response = self.client.post('/update_member_form/1', data={'member_name': 'Updated Name', 'member_email': 'updated@example.com', 'member_contact': '1234567890'})
            self.assertEqual(response.status_code, 302)

    @patch('models.storage.delete')
    @patch('models.storage.get')
    def test_delete_member(self, mock_get, mock_delete):
        """Test delete_member route"""
        mock_get.return_value = MagicMock(spec=Members)
        with self.app.app_context():
            response = self.client.get('/delete_member/1')
            self.assertEqual(response.status_code, 302)
