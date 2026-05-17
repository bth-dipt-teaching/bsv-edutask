import pytest
import unittest.mock as mock
from unittest.mock import patch, MagicMock

from src.controllers.usercontroller import UserController


@pytest.mark.unit
class TestGetUserByEmail:
    @pytest.fixture
    def mocked_dao(self):
        return MagicMock()

    @pytest.fixture
    def sut(self, mocked_dao):
        return UserController(dao=mocked_dao)

    # Test Case 1: Invalid email format (missing @)
    def test_invalid_email_missing_at(self, sut):
        with pytest.raises(ValueError, match="Error: invalid email address"):
            sut.get_user_by_email("invalidemail.com")

    # Test Case 2: Invalid email format (empty string)
    def test_invalid_email_empty(self, sut):
        with pytest.raises(ValueError, match="Error: invalid email address"):
            sut.get_user_by_email("")

    # Test Case 3: No user found with valid email
    def test_no_user_found(self, sut, mocked_dao):
        mocked_dao.find.return_value = []
        
        result = sut.get_user_by_email("notfound@example.com")
        
        assert result is None
        mocked_dao.find.assert_called_once_with({'email': 'notfound@example.com'})

    # Test Case 4: Single user found (happy path)
    def test_single_user_found(self, sut, mocked_dao):
        expected_user = {
            '_id': {'$oid': '123456789012345678901234'},
            'email': 'user@example.com',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        mocked_dao.find.return_value = [expected_user]
        
        result = sut.get_user_by_email("user@example.com")
        
        assert result == expected_user
        mocked_dao.find.assert_called_once_with({'email': 'user@example.com'})

    # Test Case 5: Multiple users found (edge case - should print warning)
    def test_multiple_users_found(self, sut, mocked_dao, capsys):
        user1 = {
            '_id': {'$oid': '123456789012345678901234'},
            'email': 'duplicate@example.com',
            'firstName': 'John',
            'lastName': 'Doe'
        }
        user2 = {
            '_id': {'$oid': '567890123456789012345678'},
            'email': 'duplicate@example.com',
            'firstName': 'Jane',
            'lastName': 'Smith'
        }
        mocked_dao.find.return_value = [user1, user2]
        
        result = sut.get_user_by_email("duplicate@example.com")
        
        assert result == user1
        captured = capsys.readouterr()
        assert "Error: more than one user found with mail duplicate@example.com" in captured.out

    # Test Case 6: Database operation failure
    def test_database_failure(self, sut, mocked_dao):
        mocked_dao.find.side_effect = Exception("Database connection failed")
        
        with pytest.raises(Exception, match="Database connection failed"):
            sut.get_user_by_email("user@example.com")

    # Test Case 7: Valid email with simple format
    def test_valid_email_simple(self, sut, mocked_dao):
        expected_user = {
            '_id': {'$oid': '123456789012345678901234'},
            'email': 'a@b.c',
            'firstName': 'Test',
            'lastName': 'User'
        }
        mocked_dao.find.return_value = [expected_user]
        
        result = sut.get_user_by_email("a@b.c")
        
        assert result == expected_user

    # Test Case 8: Email with multiple @ symbols (still matches regex pattern)
    def test_email_multiple_at(self, sut, mocked_dao):
        expected_user = {
            '_id': {'$oid': '123456789012345678901234'},
            'email': 'user@domain@example.com',
            'firstName': 'Test',
            'lastName': 'User'
        }
        mocked_dao.find.return_value = [expected_user]
        
        result = sut.get_user_by_email("user@domain@example.com")
        
        assert result == expected_user
