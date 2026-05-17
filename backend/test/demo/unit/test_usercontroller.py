import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController


def test_valid_email_one_user():
    """TC1: Valid email, 1 user found"""
    mock_dao = Mock()
    controller = UserController(dao=mock_dao)
    user = {"email": "test@example.com", "name": "Test"}
    mock_dao.find.return_value = [user]
    
    result = controller.get_user_by_email("test@example.com")
    assert result == user


def test_valid_email_multiple_users(capsys):
    """TC3: Valid email, multiple users found"""
    mock_dao = Mock()
    controller = UserController(dao=mock_dao)
    user1 = {"email": "test@example.com"}
    user2 = {"email": "test@example.com"}
    mock_dao.find.return_value = [user1, user2]
    
    result = controller.get_user_by_email("test@example.com")
    assert result == user1
    captured = capsys.readouterr()
    assert "test@example.com" in captured.out


def test_invalid_email():
    """TC4: Invalid email format"""
    mock_dao = Mock()
    controller = UserController(dao=mock_dao)
    
    with pytest.raises(ValueError):
        controller.get_user_by_email("notanemail")


def test_database_fails():
    """TC5: Database operation fails"""
    mock_dao = Mock()
    controller = UserController(dao=mock_dao)
    mock_dao.find.side_effect = Exception("DB error")
    
    with pytest.raises(Exception):
        controller.get_user_by_email("test@example.com")


def test_no_users_found():
    """TC2: Valid email, no users found"""
    mock_dao = Mock()
    controller = UserController(dao=mock_dao)
    mock_dao.find.return_value = []
    
    results = controller.get_user_by_email("test@exaple.com")
    assert result is None  
