import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


@pytest.mark.unit
def test_get_user_by_email_single_user():
    dao_mock = MagicMock()

    dao_mock.find.return_value = [{"id": "u1", "email": "test@test.com"}]

    controller = UserController(dao=dao_mock)

    result = controller.get_user_by_email("test@test.com")

    assert result["id"] == "u1"


@pytest.mark.unit
def test_get_user_by_email_multiple_users():
    dao_mock = MagicMock()

    dao_mock.find.return_value = [
        {"id": "u1", "email": "test@test.com"},
        {"id": "u2", "email": "test@test.com"},
        {"id": "u3", "email": "test@test.com"},
    ]

    controller = UserController(dao=dao_mock)

    result = controller.get_user_by_email("test@test.com")

    assert result["id"] == "u1"


@pytest.mark.unit
def test_get_user_by_email_no_users():
    """
    The test for “no users found” fails because the method attempts to access users[0]
    even when the DAO returns an empty list. This leads to an IndexError.
    The defect is in the missing handling of the empty result case.
    """
    dao_mock = MagicMock()
    dao_mock.find.return_value = []

    controller = UserController(dao=dao_mock)

    result = controller.get_user_by_email("test@test.com")

    assert result is None
