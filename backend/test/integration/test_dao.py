import pytest
from src.util.dao import DAO


# Fixture: creates a test database collection and cleans it after tests
@pytest.fixture
def test_dao():
    dao = DAO("test_collection")  # separate test collection
    yield dao
    dao.drop()  # cleanup after test


# Test 1: Valid data be inserted successfully
def test_create_valid(test_dao):
    data = {
        "name": "John",
        "email": "john@test.com"
    }

    result = test_dao.create(data)

    assert result is not None
    assert result["name"] == "John"


# Test 2: Missing required field (depends on validator)
def test_create_missing_field(test_dao):
    data = {
        "name": "John"
    }

    with pytest.raises(Exception):
        test_dao.create(data)


# Test 3: Invalid data type (depends on validator)
def test_create_invalid_type(test_dao):
    data = {
        "name": 123   # should be string
    }

    with pytest.raises(Exception):
        test_dao.create(data)