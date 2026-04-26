import pytest
from pymongo.errors import WriteError

from src.util.dao import DAO


@pytest.fixture
def user_dao():
    dao = DAO("user")
    dao.drop()

    dao = DAO("user")
    yield dao

    dao.drop()


def test_create_valid_user(user_dao):
    data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com"
    }

    result = user_dao.create(data)

    assert result is not None
    assert result["firstName"] == "Jane"
    assert result["lastName"] == "Doe"
    assert result["email"] == "jane.doe@example.com"
    assert "_id" in result


def test_create_user_missing_required_field(user_dao):
    data = {
        "firstName": "Jane",
        "email": "jane.doe@example.com"
    }

    with pytest.raises(WriteError):
        user_dao.create(data)


def test_create_user_wrong_data_type(user_dao):
    data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": 123
    }

    with pytest.raises(WriteError):
        user_dao.create(data)


def test_create_user_with_tasks_wrong_data_type(user_dao):
    data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com",
        "tasks": "not-an-array"
    }

    with pytest.raises(WriteError):
        user_dao.create(data)