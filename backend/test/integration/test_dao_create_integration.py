import pytest
from pymongo.errors import WriteError

from src.util.dao import DAO

@pytest.fixture
def user_dao():
    dao = DAO("user_test")
    dao.drop()
    dao = DAO("user_test")

    yield dao

    dao.drop()

def test_create_valid_user(user_dao):
    data = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com"
    }

    result = user_dao.create(data)

    assert result["firstName"] == "Test"
    assert result["lastName"] == "User"
    assert result["email"] == "test@example.com"
    assert "_id" in result

def test_create_missing_last_name_fails(user_dao):
    data = {
        "firstName": "Test",
        "email": "test@example.com"
    }

    with pytest.raises(WriteError):
        user_dao.create(data)

def test_create_missing_first_name_fails(user_dao):
    data = {
        "lastName": "User",
        "email": "test@example.com"
    }

    with pytest.raises(WriteError):
        user_dao.create(data)

def test_create_missing_email_fails(user_dao):
    data = {
        "firstName": "Test",
        "lastName": "User"
    }

    with pytest.raises(WriteError):
        user_dao.create(data)

def test_create_incorrect_type_fails(user_dao):
    data = {
        "firstName": "Test",
        "lastName": 111,
        "email": "test@example.com"
    }

    with pytest.raises(WriteError):
        user_dao.create(data)