from unittest.mock import MagicMock
import pytest
from src.controllers.usercontroller import UserController

class TestUserController:
    def test_get_user_by_email_valid(self):
        # 1. Setup: Create a fake DAO and a fake user list
        mock_dao = MagicMock()
        mock_user = {'email': 'test@edutask.com', 'firstName': 'Nanda'}
        mock_dao.find.return_value = [mock_user]
        
        # 2. Initialize: Pass the fake DAO into the real Controller
        sut = UserController(dao=mock_dao)
        
        # 3. Act: Run the method
        result = sut.get_user_by_email('test@edutask.com')
        
        # 4. Assert: Check if it returned the user correctly
        assert result['email'] == 'test@edutask.com'
        mock_dao.find.assert_called_once_with({'email': 'test@edutask.com'})

    def test_get_user_by_email_empty(self):
        # This tests your fix! (Returning None when no user is found)
        mock_dao = MagicMock()
        mock_dao.find.return_value = [] # Empty list
        
        sut = UserController(dao=mock_dao)
        result = sut.get_user_by_email('nonexistent@edutask.com')
        
        # If your code is fixed, this will pass
        assert result is None
    def test_get_user_by_email_invalid_format(self):
     """ Verification of email validation logic"""
    mock_dao = MagicMock()
    sut = UserController(dao=mock_dao)
    with pytest.raises(ValueError):
        sut.get_user_by_email("not-an-email")