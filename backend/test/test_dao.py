import pytest
import os
from src.util.dao import DAO

@pytest.fixture(scope="function")
def dao():
    os.environ["MONGO_URL"] = "mongodb://localhost:27017"

    test_dao = DAO("user")
    test_dao.drop()

    test_dao = DAO("user")

    yield test_dao
    test_dao.drop()

# Test case 1
def test_missing_field(dao):
    data = {
        "lastName": "Ramos",
        "email": "ramos@example.com"
    }

    with pytest.raises(Exception):
        dao.create(data)

# Test case 2
def test_invalid_type(dao):
    data = {
        "firstName": 123,
        "lastName": "Yamal",
        "email": "yamal@example.com"
    }

    with pytest.raises(Exception):
        dao.create(data)

# Test case 3
def test_duplicate_email(dao):
    data1 = {
        "firstName": "Arda",
        "lastName": "Guler",
        "email": "same@example.com"
    }

    data2 = {
        "firstName": "Another",
        "lastName": "User",
        "email": "same@example.com"
    }

    dao.create(data1)
    result = dao.create(data2)

    assert result["email"] == "same@example.com"

# Test case 4
def test_valid(dao):
    data = {
        "firstName": "Cristiano",
        "lastName": "Ronaldo",
        "email": "ronaldo@example.com"
    }

    result = dao.create(data)

    assert result["firstName"] == "Cristiano"
    assert result["email"] == "ronaldo@example.com"
    assert "_id" in result
