import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def user_controller():
    dao_mock = MagicMock()
    return UserController(dao=dao_mock)

@pytest.mark.unit
def test_invalid_email(user_controller):
    with pytest.raises(ValueError):
        user_controller.get_user_by_email("invalidemail")

@pytest.mark.unit
def test_no_user_found(user_controller):
    user_controller.dao.find.return_value = []
    result = user_controller.get_user_by_email("test@example.com")
    assert result is None

@pytest.mark.unit
def test_one_user_found(user_controller):
    fake_user = {"email": "test@example.com", "name": "Test"}
    user_controller.dao.find.return_value = [fake_user]
    result = user_controller.get_user_by_email("test@example.com")
    assert result == fake_user

@pytest.mark.unit
def test_multiple_users_found(user_controller):
    fake_user1 = {"email": "test@example.com", "name": "Test1"}
    fake_user2 = {"email": "test@example.com", "name": "Test2"}
    user_controller.dao.find.return_value = [fake_user1, fake_user2]
    result = user_controller.get_user_by_email("test@example.com")
    assert result == fake_user1

@pytest.mark.unit
def test_database_exception(user_controller):
    user_controller.dao.find.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        user_controller.get_user_by_email("test@example.com")
