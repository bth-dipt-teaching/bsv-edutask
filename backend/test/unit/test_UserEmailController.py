import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    """
    This creates a MOCK object that replaces the real DAO.
    """
    return MagicMock()

@pytest.fixture
def controller(mock_dao):
    """
    Inject the mocked DAO into the controller.
    """
    return UserController(dao=mock_dao)

@pytest.mark.unit
def test_get_user_by_email_single_user(controller, mock_dao):

    mock_dao.find.return_value = [{"id": "u1", "email": "test@test.com"}]

    result = controller.get_user_by_email("test@test.com")

    assert result["id"] == "u1"

@pytest.mark.unit
def test_get_user_by_email_multiple_users(controller, mock_dao):

    mock_dao.find.return_value = [
        {"id": "u1", "email": "test@test.com"},
        {"id": "u2", "email": "test@test.com"},
        {"id": "u3", "email": "test@test.com"},
    ]

    result = controller.get_user_by_email("test@test.com")

    assert result["id"] == "u1"

@pytest.mark.unit
def test_get_user_by_email_no_users(controller, mock_dao):
    """
    The test for “no users found” fails because the method attempts to access users[0]
    even when the DAO returns an empty list. This leads to an IndexError.
    The defect is in the missing handling of the empty result case.
    """
    mock_dao.find.return_value = []

    result = controller.get_user_by_email("test@test.com")

    assert result is None

@pytest.mark.unit
@pytest.mark.parametrize("email", [
    "invalidemail",
    "test@",
    "@example.com",
    "test@@example.com",
    "",
])
def test_invalid_emails_should_raise_value_error(controller, email):
    with pytest.raises(ValueError):
        controller.get_user_by_email(email)

@pytest.mark.unit
def test_dao_exception_propagation(controller, mock_dao):
    mock_dao.find.side_effect = Exception("Database failure")

    with pytest.raises(Exception):
        controller.get_user_by_email("test@example.com")