import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController


@pytest.fixture
def mock_dao():
    return Mock()


@pytest.fixture
def controller(mock_dao):
    return UserController(mock_dao)


def test_when_one_match_exists(controller, mock_dao):
    fake_user = {"email": "test@example.com", "name": "Sabor"}
    mock_dao.find.return_value = [fake_user]

    result = controller.get_user_by_email("test@example.com")

    assert result == fake_user


def test_when_no_user_exists(controller, mock_dao):
    mock_dao.find.return_value = []

    result = controller.get_user_by_email("test@example.com")

    assert result is None


def test_when_multiple_users_exist_and_print_warning(controller, mock_dao, capsys):
    fake_user1 = {"email": "test@example.com", "name": "Sabor"}
    fake_user2 = {"email": "test@example.com", "name": "Another User"}
    mock_dao.find.return_value = [fake_user1, fake_user2]

    result = controller.get_user_by_email("test@example.com")

    captured = capsys.readouterr()

    assert result == fake_user1
    assert "more than one user found" in captured.out


def test_raises_value_error_for_invalid_email(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid email")


def test_raises_exception_when_dao_fails(controller, mock_dao):
    mock_dao.find.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        controller.get_user_by_email("test@example.com")