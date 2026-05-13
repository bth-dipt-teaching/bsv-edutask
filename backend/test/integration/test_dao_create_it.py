import pytest
from unittest import mock
from pymongo.mongo_client import MongoClient
from pymongo.errors import WriteError
from unittest.mock import patch
from src.util.dao import DAO

#Simple validator mock, to test enforcement (not testing file loading functionality)
@pytest.fixture
def validator():
    return {
            "$jsonSchema": {
            "bsonType": "object",
            "required": ["username"],
            "properties": {
                "username": {
                    "bsonType": "string",
                    "description": "the first name of a user must be determined",
                    "uniqueItems": True
                }, 
                "logged_in": {
                    "bsonType": "bool",
                    "description": "flag for whether user is currently logged in"
                },
            }
        }
    }

@pytest.fixture 
def patcher(validator):
    with patch("src.util.dao.getValidator") as Validator,\
        patch("src.util.dao.pymongo.MongoClient") as db_client:
        Validator.return_value = validator
        # Patch the database instance from edutask -> test_db, to not affect the prod instance.
        prod_client = MongoClient("mongodb://localhost:27017")
        prod_client.edutask = prod_client.test_db
        db_client.return_value = prod_client
        yield
        #Drop the test database to clean up.
        prod_client.drop_database("test_db")

@pytest.fixture 
def dao(patcher):
    dao = DAO("test_collection")
    yield dao
    dao.drop()

@pytest.mark.integration
class TestDaoCreateIT:

    @pytest.mark.parametrize("valid_obj", [
        ({"username" : "bob", "logged_in" : True}),
        ({"username" : "bob"})
    ])
    def test_create_valid(self, dao : DAO, valid_obj):
        #Arrange
        #Act
        res = dao.create(valid_obj)

        #Assert
        assert res["_id"]
        assert res["username"] == valid_obj["username"]

    @pytest.mark.parametrize("invalid_obj", [
        ({}),
        ({"username" : "sando", "logged_in" : "Yes"}),
        ({"lastname" : "bob", "logged_in" : False}),
        ({"logged_in" : True}),
        ({"username" : 4}),
    ])
    def test_create_write_error(self, dao : DAO, invalid_obj):
        #Arrange
        #Act
        with pytest.raises(WriteError):
            #Assert
            dao.create(invalid_obj)
    
    #username is set as uniqueItems as per the existing validators. 
    # According to function description the duplicate should throw write error.
    #Fails because of how mongoDB unique items work by default:
    #"Keyword    | Type   | Definition | Behavior
    #uniqueItems | arrays | boolean    | If true, each item in the array must be unique. Otherwise, no uniqueness constraint is enforced."
    #I.e ensure uniquness of items in arrays not across documents.
    def test_create_duplicate_document(self, dao : DAO):
        #Arrange 
        existing_obj = {"username": "A",  "logged_in" : False}
        dao.create(existing_obj)
        duplicate = {"username": "A",  "logged_in" : True}
        #Act
        with pytest.raises(WriteError):
            #Assert
            dao.create(duplicate)