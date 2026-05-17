from unittest.mock import Mock

import pytest

from src.controllers.usercontroller import UserController


pytestmark = pytest.mark.unit


@pytest.fixture
def dao():
    return Mock()


@pytest.fixture
def controller(dao):
    return UserController(dao)


def test_get_user_by_email_returns_user_for_registered_valid_email(controller, dao):
    user = {
        "_id": "user-1",
        "firstName": "Anna",
        "lastName": "Andersson",
        "email": "anna@example.com",
    }
    dao.find.return_value = [user]

    result = controller.get_user_by_email("anna@example.com")

    assert result == user
    dao.find.assert_called_once_with({"email": "anna@example.com"})


def test_get_user_by_email_returns_none_for_unregistered_valid_email(controller, dao):
    dao.find.return_value = []

    result = controller.get_user_by_email("missing@example.com")

    assert result is None
    dao.find.assert_called_once_with({"email": "missing@example.com"})


def test_get_user_by_email_returns_first_user_and_warns_when_multiple_match(
    controller, dao, capsys
):
    first_user = {
        "_id": "user-1",
        "firstName": "Anna",
        "lastName": "Andersson",
        "email": "duplicate@example.com",
    }
    second_user = {
        "_id": "user-2",
        "firstName": "Bo",
        "lastName": "Bengtsson",
        "email": "duplicate@example.com",
    }
    dao.find.return_value = [first_user, second_user]

    result = controller.get_user_by_email("duplicate@example.com")

    assert result == first_user
    assert "duplicate@example.com" in capsys.readouterr().out


def test_get_user_by_email_rejects_email_without_at_sign(controller, dao):
    with pytest.raises(ValueError):
        controller.get_user_by_email("anna.example.com")

    dao.find.assert_not_called()


def test_get_user_by_email_rejects_email_without_domain_host(controller, dao):
    with pytest.raises(ValueError):
        controller.get_user_by_email("anna@example")

    dao.find.assert_not_called()


def test_get_user_by_email_forwards_database_failure(controller, dao):
    dao.find.side_effect = RuntimeError("database unavailable")

    with pytest.raises(RuntimeError, match="database unavailable"):
        controller.get_user_by_email("anna@example.com")
