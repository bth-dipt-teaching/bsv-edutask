import pytest
from src.util.dao import DAO


@pytest.fixture
def test_dao():
    dao = DAO("user")

    dao.collection.delete_many({})

    yield dao

    dao.collection.delete_many({})


def test_create_valid_object(test_dao):
    data = {
        "email": "test@mail.com",
        "firstName": "Test",
        "lastName": "User"
    }

    result = test_dao.create(data)

    assert result["email"] == "test@mail.com"
    assert result["firstName"] == "Test"
    assert result["lastName"] == "User"
    assert "_id" in result


def test_create_missing_required_field(test_dao):
    data = {
        "email": "test@mail.com",
        "firstName": "Test"
    }

    with pytest.raises(Exception):
        test_dao.create(data)


def test_create_wrong_data_type(test_dao):
    data = {
        "email": "test@mail.com",
        "firstName": "Test",
        "lastName": 123
    }

    with pytest.raises(Exception):
        test_dao.create(data)


def test_create_duplicate_value(test_dao):
    data = {
        "email": "test@mail.com",
        "firstName": "Test",
        "lastName": "User"
    }

    first = test_dao.create(data)
    second = test_dao.create(data)

    assert first["email"] == second["email"]
    assert first["_id"] != second["_id"]