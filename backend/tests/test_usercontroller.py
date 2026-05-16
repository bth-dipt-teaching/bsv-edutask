import pytest
from unittest.mock import Mock

from src.controllers.usercontroller import UserController


def test_get_user_by_email_returns_user_when_one_match_exists():
    user = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com"
    }

    dao = Mock()
    dao.find.return_value = [user]

    controller = UserController(dao=dao)
    result = controller.get_user_by_email("jane.doe@example.com")

    assert result == user
    dao.find.assert_called_once_with({"email": "jane.doe@example.com"})


def test_get_user_by_email_returns_none_when_no_user_exists():
    dao = Mock()
    dao.find.return_value = []

    controller = UserController(dao=dao)
    result = controller.get_user_by_email("missing@example.com")

    assert result is None
    dao.find.assert_called_once_with({"email": "missing@example.com"})


def test_get_user_by_email_returns_first_user_when_multiple_users_exist():
    first_user = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "duplicate@example.com"
    }
    second_user = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "duplicate@example.com"
    }

    dao = Mock()
    dao.find.return_value = [first_user, second_user]

    controller = UserController(dao=dao)
    result = controller.get_user_by_email("duplicate@example.com")

    assert result == first_user
    dao.find.assert_called_once_with({"email": "duplicate@example.com"})


def test_get_user_by_email_raises_value_error_for_invalid_email():
    dao = Mock()

    controller = UserController(dao=dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")

    dao.find.assert_not_called()


def test_get_user_by_email_raises_value_error_for_email_without_host():
    dao = Mock()

    controller = UserController(dao=dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid@example")

    dao.find.assert_not_called()