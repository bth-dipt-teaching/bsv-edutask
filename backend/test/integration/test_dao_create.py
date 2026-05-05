import pytest
from bson import ObjectId
from pymongo.errors import WriteError
from unittest.mock import patch

from src.util.dao import DAO


def extract_id(doc: any) -> ObjectId:
    return ObjectId(doc["_id"]["$oid"])


@pytest.fixture
def dao_no_validator():
    with patch("src.util.validators.getValidator") as mock_validator:
        mock_validator.return_value = {}
        dao = DAO("user")
        yield dao
        dao.drop()

@pytest.fixture
def dao_strict_validator():
    strict_schema = {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                "bsonType": "string",
                "description": "the first name of a user must be determined"
            }, 
            "lastName": {
                "bsonType": "string",
                "description": "the last name of a user must be determined"
            },
            "email": {
                "bsonType": "string",
                "description": "the email address of a user must be determined",
                "uniqueItems": True
            },
            "tasks": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            }
        }
    }

    with patch("src.util.validators.getValidator") as mock_validator:
        mock_validator.return_value = strict_schema
        dao = DAO("user")
        yield dao
        dao.drop()

@pytest.mark.integration
def test_no_required_fields(dao_strict_validator):
    # arrange
    new_house = {
        "Address": "1428 Elm Street",
        "City": "Ohio",
        "Owner": "Nancy Thompson"
    }
    
    # act & assert
    with pytest.raises(WriteError):
        dao_strict_validator.create(new_house)


# @pytest.mark.integration
# def test_full_valid(dao, task_dao):
#     # arrange
#     task_id1 = extract_id(
#         task_dao.create({"title": "test1", "description": "test task 1"})
#     )

#     task_id2 = extract_id(
#         task_dao.create({"title": "test2", "description": "test task 2"})
#     )

#     new_user = {
#         "firstName": "Mattias",
#         "lastName": "Larsson",
#         "email": "mattias.larsson@example.com",
#         "tasks": [task_id1, task_id2],
#     }

#     # act
#     inserted_user = dao.create(new_user)

#     # assert
#     assert inserted_user != None
#     assert inserted_user["firstName"] == new_user["firstName"]
#     assert inserted_user["lastName"] == new_user["lastName"]
#     assert inserted_user["email"] == new_user["email"]
#     assert [ObjectId(t["$oid"]) for t in inserted_user["tasks"]] == [task_id1, task_id2]


# @pytest.mark.integration
# def test_minimal_valid_doc(dao):
#     # arrange
#     new_user = {
#         "firstName": "Mattias",
#         "lastName": "Larsson",
#         "email": "mattias.larsson@example.com",
#     }

#     # act
#     inserted_user = dao.create(new_user)

#     # assert
#     assert inserted_user != None
#     assert inserted_user["firstName"] == new_user["firstName"]
#     assert inserted_user["lastName"] == new_user["lastName"]
#     assert inserted_user["email"] == new_user["email"]


# @pytest.mark.integration
# def test_missing_fields_doc(dao):
#     # arrange
#     new_user = {
#         "firstName": "Mattias",
#         "lastName": "Larsson",
#     }

#     # act & assert
#     with pytest.raises(WriteError):
#         dao.create(new_user)


# @pytest.mark.integration
# def test_wrong_type(dao):
#     # arrange
#     new_user = {"firstName": True, "lastName": 10.0, "email": ["testing@example.com"]}

#     # act & assert
#     with pytest.raises(WriteError):
#         dao.create(new_user)


# @pytest.mark.integration
# def test_extra_field(dao):
#     # arrange
#     new_user = {
#         "firstName": "Mattias",
#         "lastName": "Larsson",
#         "email": "mattias.larsson@example.com",
#         "hacked": True,
#     }

#     # act & assert
#     with pytest.raises(WriteError):
#         dao.create(new_user)


# @pytest.mark.integration
# def test_unique_field(dao):
#     # arrange
#     new_user = {
#         "firstName": "Mattias",
#         "lastName": "Larsson",
#         "email": "mattias.larsson@example.com",
#     }

#     # act
#     dao.create(new_user)

#     # assert
#     with pytest.raises(WriteError):
#         dao.create(new_user)


# @pytest.mark.integration
# def test_empty_dict(dao):
#     # arrange
#     new_user = {}

#     # act & assert
#     with pytest.raises(WriteError):
#         dao.create(new_user)


# @pytest.mark.integration
# def test_invalid_bson(dao):
#     # arrange
#     new_user = {
#         "firstName": "Mattias",
#         "lastName": "Larsson",
#         "email": "test@example.com",
#         "tasks": ["not-a-valid-objectid"],
#     }

#     # act & assert
#     with pytest.raises(WriteError):
#         dao.create(new_user)
