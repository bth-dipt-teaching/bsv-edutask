from unittest.mock import Mock
import pytest

from src.controllers.usercontroller import UserController


def test_get_user_by_email_found():
    dao = Mock()
    user = {
        "email": "test@mail.com",
        "firstName": "Test",
        "lastName": "User"
    }
    dao.find.return_value = [user]

    controller = UserController(dao)

    result = controller.get_user_by_email("test@mail.com")

    assert result == user
    dao.find.assert_called_once_with({"email": "test@mail.com"})


def test_get_user_by_email_not_found():
    dao = Mock()
    dao.find.return_value = []

    controller = UserController(dao)

    result = controller.get_user_by_email("missing@mail.com")

    assert result is None


def test_get_user_by_email_multiple_users_returns_first():
    dao = Mock()
    first_user = {"email": "test@mail.com", "firstName": "First"}
    second_user = {"email": "test@mail.com", "firstName": "Second"}
    dao.find.return_value = [first_user, second_user]

    controller = UserController(dao)

    result = controller.get_user_by_email("test@mail.com")

    assert result == first_user


def test_get_user_by_email_invalid_email():
    dao = Mock()
    controller = UserController(dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")