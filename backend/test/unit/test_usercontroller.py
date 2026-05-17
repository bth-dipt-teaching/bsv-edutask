import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController


pytestmark = pytest.mark.unit

@pytest.fixture
def sut():
    mock_dao = MagicMock()
    controller = UserController(dao=mock_dao)
    return controller, mock_dao


def test_get_user_by_email_single_result(sut):
    controller, mock_dao = sut
    user = {"email": "test@example.com", "name": "Alice"}
    mock_dao.find.return_value = [user]

    result = controller.get_user_by_email("test@example.com")

    assert result == user
    mock_dao.find.assert_called_once_with({"email": "test@example.com"})


def test_get_user_by_email_no_result(sut):
    controller, mock_dao = sut
    mock_dao.find.return_value = []

    result = controller.get_user_by_email("nobody@example.com")

    assert result is None
    mock_dao.find.assert_called_once_with({"email": "nobody@example.com"})


def test_get_user_by_email_multiple_results_returns_first_user(sut):
    controller, mock_dao = sut
    user1 = {"email": "dup@example.com", "name": "Alice"}
    user2 = {"email": "dup@example.com", "name": "Bob"}
    mock_dao.find.return_value = [user1, user2]

    result = controller.get_user_by_email("dup@example.com")

    assert result == user1
    mock_dao.find.assert_called_once_with({"email": "dup@example.com"})


def test_get_user_by_email_invalid_email_raises_value_error(sut):
    controller, mock_dao = sut

    with pytest.raises(ValueError):
        controller.get_user_by_email("notanemail")

    mock_dao.find.assert_not_called()


def test_get_user_by_email_email_without_host_raises_value_error(sut):
    controller, mock_dao = sut

    with pytest.raises(ValueError):
        controller.get_user_by_email("test@example")

    mock_dao.find.assert_not_called()


def test_get_user_by_email_empty_string_raises_value_error(sut):
    controller, mock_dao = sut

    with pytest.raises(ValueError):
        controller.get_user_by_email("")

    mock_dao.find.assert_not_called()


def test_get_user_by_email_forwards_dao_exception(sut):
    controller, mock_dao = sut
    mock_dao.find.side_effect = RuntimeError("database unavailable")

    with pytest.raises(RuntimeError):
        controller.get_user_by_email("test@example.com")
