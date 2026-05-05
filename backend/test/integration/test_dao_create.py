import pytest
from pymongo.errors import WriteError
from unittest.mock import patch

from src.util.dao import DAO


@pytest.fixture
def dao_no_validator():
    with patch("src.util.dao.getValidator") as mock_validator:
        mock_validator.return_value = {}
        dao = DAO("user")
        dao.drop()
        dao = DAO("user")

        yield dao
        dao.drop()


@pytest.fixture
def dao_strict_validator():
    strict_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["firstName", "lastName", "email"],
            "additionalProperties": False,
            "properties": {
                "_id": {"bsonType": "objectId"},
                "firstName": {
                    "bsonType": "string",
                    "description": "the first name of a user must be determined",
                },
                "lastName": {
                    "bsonType": "string",
                    "description": "the last name of a user must be determined",
                },
                "email": {
                    "bsonType": "string",
                    "description": "the email address of a user must be determined",
                    "uniqueItems": True,
                },
                "tasks": {"bsonType": "array", "items": {"bsonType": "objectId"}},
            },
        }
    }

    with patch("src.util.dao.getValidator") as mock_validator:
        mock_validator.return_value = strict_schema
        dao = DAO("user")
        dao.drop()
        dao = DAO("user")

        yield dao
        dao.drop()


@pytest.mark.integration
def test_no_required_fields(dao_strict_validator):
    # arrange
    new_house = {
        "Address": "1428 Elm Street",
        "City": "Ohio",
        "Owner": "Nancy Thompson",
    }

    # act & assert
    with pytest.raises(WriteError):
        dao_strict_validator.create(new_house)


@pytest.mark.integration
def test_wrong_type(dao_strict_validator):
    # arrange
    new_user = {"firstName": True, "lastName": 123, "email": ["arr"]}

    # act & assert
    with pytest.raises(WriteError):
        dao_strict_validator.create(new_user)


@pytest.mark.integration
def test_extra_fields(dao_strict_validator):
    # arrange
    new_user = {
        "firstName": "Joe",
        "lastName": "Smith",
        "email": "email@email.com",
        "Address": "Street 123",
    }

    # act & assert
    with pytest.raises(WriteError):
        dao_strict_validator.create(new_user)


@pytest.mark.integration
def test_correct_required_fields(dao_strict_validator):
    required_fields_filled = {
        "firstName": "Joe",
        "lastName": "Smith",
        "email": "email@email.com",
    }
    result = dao_strict_validator.create(required_fields_filled)

    assert result is not None
    assert "_id" in result
    assert result["firstName"] == "Joe"
    assert result["lastName"] == "Smith"
    assert result["email"] == "email@email.com"
