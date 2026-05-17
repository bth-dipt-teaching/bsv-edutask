from unittest.mock import MagicMock
import pytest
from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    return MagicMock()


def test_single_user(mock_dao):
    mock_dao.find.return_value = [{"email": "user@test.com"}]

    controller = UserController(mock_dao)
    result = controller.get_user_by_email("user@test.com")

    assert result["email"] == "user@test.com"


def test_multiple_users(mock_dao):
    mock_dao.find.return_value = [
        {"email": "user@test.com"},
        {"email": "user@test.com"}
    ]

    controller = UserController(mock_dao)
    result = controller.get_user_by_email("user@test.com")

    assert result["email"] == "user@test.com"


def test_invalid_email(mock_dao):
    controller = UserController(mock_dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")


def test_no_user_found(mock_dao):
    mock_dao.find.return_value = []

    controller = UserController(mock_dao)

    with pytest.raises(IndexError):
        controller.get_user_by_email("user@test.com")