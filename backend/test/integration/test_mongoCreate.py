import pytest
from pymongo.errors import WriteError
from bson import ObjectId
from pathlib import Path
import json
from unittest.mock import patch

from src.util.dao import DAO


@pytest.fixture
def validator():
    path = Path("src/static/validators/user.json")
    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture
def test_dao(validator):
    with patch("src.util.dao.getValidator", return_value=validator):
        dao = DAO("testing_integrtion")
        yield dao
        dao.drop()


@pytest.mark.integration
def test_create_valid_user(test_dao):
    data = {"firstName": "John", "lastName": "Doe", "email": "john@example.com"}

    result = test_dao.create(data)

    assert result["firstName"] == "John"
    assert result["lastName"] == "Doe"
    assert result["email"] == "john@example.com"
    assert "_id" in result


@pytest.mark.integration
def test_create_valid_user_with_tasks(test_dao):
    data = {
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane@example.com",
        "tasks": [ObjectId()],
    }

    result = test_dao.create(data)

    assert result["tasks"] is not None


@pytest.mark.integration
def test_extra_field_allowed(test_dao):
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john3@example.com",
        "number": 21,
    }

    result = test_dao.create(data)

    assert result["number"] == 21


@pytest.mark.integration
def test_missing_firstname(test_dao):
    data = {"lastName": "Doe", "email": "john@example.com"}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_missing_lastname(test_dao):
    data = {"firstName": "John", "email": "john@example.com"}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_missing_email(test_dao):
    data = {"firstName": "John", "lastName": "Doe"}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_empty_user(test_dao):
    with pytest.raises(WriteError):
        test_dao.create({})


@pytest.mark.integration
def test_wrong_type_firstname(test_dao):
    data = {"firstName": 123, "lastName": "Doe", "email": "john@example.com"}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_wrong_type_lastname(test_dao):
    data = {"firstName": "John", "lastName": True, "email": "john@example.com"}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_wrong_type_email(test_dao):
    data = {"firstName": "John", "lastName": "Doe", "email": False}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_null_email(test_dao):
    data = {"firstName": "John", "lastName": "Doe", "email": None}

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_tasks_not_array(test_dao):
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "tasks": "not_array",
    }

    with pytest.raises(WriteError):
        test_dao.create(data)


@pytest.mark.integration
def test_tasks_wrong_item_type(test_dao):
    data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "tasks": ["not_objectid"],
    }

    with pytest.raises(WriteError):
        test_dao.create(data)

@pytest.mark.integration
def test_duplicate_email_should_fail(test_dao):
    data = {"firstName": "John", "lastName": "Doe", "email": "dup@example.com"}

    test_dao.create(data)

    with pytest.raises(WriteError):
        test_dao.create(data)
