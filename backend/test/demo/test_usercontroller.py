import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController


def test_user_found():
    dao = Mock()
    dao.find.return_value = [{"email": "test@mail.com"}]

    controller = UserController(dao)

    result = controller.get_user_by_email("test@mail.com")

    assert result == {"email": "test@mail.com"}


def test_user_not_found():
    dao = Mock()
    dao.find.return_value = []

    controller = UserController(dao)

    result = controller.get_user_by_email("missing@mail.com")

    assert result is None


def test_multiple_users():
    dao = Mock()
    dao.find.return_value = [
        {"email": "test@mail.com"},
        {"email": "test@mail.com"}
    ]

    controller = UserController(dao)

    result = controller.get_user_by_email("test@mail.com")

    assert result == {"email": "test@mail.com"}


def test_invalid_email():
    dao = Mock()
    controller = UserController(dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("")