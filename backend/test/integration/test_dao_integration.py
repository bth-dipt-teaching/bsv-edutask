import pytest
from src.util.dao import DAO
from unittest.mock import patch
from pymongo.errors import WriteError

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                "bsonType": "string",
            }, 
            "lastName": {
                "bsonType": "string",
            },
            "email": {
                "bsonType": "string",
            }
        }
    }
}
@pytest.fixture
def dao():
    with patch('src.util.dao.getValidator') as mock_validator:
        mock_validator.return_value = validator
        dao = DAO("user")
        dao.drop()
        dao = DAO("user")

        dao.collection.create_index("email", unique=True)
        yield dao
        dao.drop()

@pytest.mark.integration
def test_create_valid_user(dao):
    data = {
        "firstName": "name",
        "lastName": "Test",
        "email": "name@test.com"
    }

    result = dao.create(data)

    assert result is not None
    assert result["firstName"] == "name"
    assert result["lastName"] == "Test"
    assert result["email"] == "name@test.com"
    assert "_id" in result

@pytest.mark.integration
def test_create_missing_field(dao):
    data = {
        "firstName": "name",
        "email": "name@test.com"
    }

    with pytest.raises(WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_wrong_type(dao):
    data = {
        "firstName": "name",
        "lastName": "Test",
        "email": 12345 
    }

    with pytest.raises(WriteError):
        dao.create(data)

@pytest.mark.integration
def test_create_duplicate_email(dao):
    data = {
        "firstName": "name",
        "lastName": "Test",
        "email": "name@test.com"
    }

    dao.create(data)
    
    with pytest.raises(WriteError):
        dao.create(data)
