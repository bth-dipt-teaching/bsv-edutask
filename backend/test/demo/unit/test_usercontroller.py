import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

FAKE_USER = {
    "name": "Test User",
    "email": "testuser@example.com"
}

@pytest.fixture
def controller():
    dao = MagicMock()
    return UserController(dao=dao)


def test_valid_email_found(controller):
    controller.dao.find.return_value = [FAKE_USER]
    result = controller.get_user_by_email("testuser@example.com")
    assert result["email"] == "testuser@example.com"


def test_email_not_found_should_return_none(controller):
    controller.dao.find.return_value = []
    result = controller.get_user_by_email("nobody@example.com")
    assert result is None   # this will fail


def test_invalid_email_format(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid")


def test_empty_email(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("")


def test_none_email(controller):
    with pytest.raises(Exception):
        controller.get_user_by_email(None)