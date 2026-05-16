import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController


# Creates fake DAO.
@pytest.fixture
def mock_dao():
    return Mock()


# Creates controller with mocked DAO.
@pytest.fixture
def controller(mock_dao):
    return UserController(mock_dao)


# Returns user when one match exists.
def test_single_user_found(controller, mock_dao):
    mock_dao.find.return_value = [{"email": "john@test.com"}]

    result = controller.get_user_by_email("john@test.com")

    assert result["email"] == "john@test.com"


# Invalid email should raise ValueError.
def test_invalid_email_raises_value_error(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("wrong-email")


# Accepts current behavior for @test.com.
def test_invalid_email_missing_local_part(controller, mock_dao):
    mock_dao.find.return_value = []

    with pytest.raises(ValueError):
        controller.get_user_by_email("@test.com")


# Only failing test: no user should return None.
def test_no_user_found_returns_none(controller, mock_dao):
    mock_dao.find.return_value = []

    result = controller.get_user_by_email("none@test.com")

    assert result is None
    

# DAO errors should be propagated.
def test_database_exception_propagates(controller, mock_dao):
    mock_dao.find.side_effect = Exception("Database failed")

    with pytest.raises(Exception):
        controller.get_user_by_email("test@test.com")