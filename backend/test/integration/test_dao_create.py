import os

import pytest
import pymongo
from bson import ObjectId
from pymongo.errors import WriteError

from src.util.dao import DAO


TEST_MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
TEST_COLLECTION = "user"


@pytest.fixture
def user_dao():
    """
    Creates a DAO connected to a test MongoDB instance and a clean user collection.

    The fixture avoids disturbing production data by overriding the MONGO_URL
    environment variable so the DAO connects to the test MongoDB instance.
    The user collection is dropped before and after each test so every test
    starts from a clean database state.
    """
    previous_mongo_url = os.environ.get("MONGO_URL")
    os.environ["MONGO_URL"] = TEST_MONGO_URL

    client = pymongo.MongoClient(TEST_MONGO_URL)
    database = client.edutask

    if TEST_COLLECTION in database.list_collection_names():
        database.drop_collection(TEST_COLLECTION)

    dao = DAO(collection_name=TEST_COLLECTION)

    yield dao

    dao.drop()
    client.close()

    if previous_mongo_url is None:
        os.environ.pop("MONGO_URL", None)
    else:
        os.environ["MONGO_URL"] = previous_mongo_url


def valid_user(email="alice@example.com"):
    return {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": email
    }


def test_create_valid_user(user_dao):
    created_user = user_dao.create(valid_user())

    assert "_id" in created_user
    assert "$oid" in created_user["_id"]
    assert ObjectId.is_valid(created_user["_id"]["$oid"])

    assert created_user["firstName"] == "Alice"
    assert created_user["lastName"] == "Andersson"
    assert created_user["email"] == "alice@example.com"


def test_create_user_with_missing_required_property(user_dao):
    invalid_user = {
        "firstName": "Alice",
        "lastName": "Andersson"
    }

    with pytest.raises(WriteError):
        user_dao.create(invalid_user)


def test_create_user_with_wrong_bson_type(user_dao):
    invalid_user = {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": 123
    }

    with pytest.raises(WriteError):
        user_dao.create(invalid_user)


def test_create_user_with_duplicate_unique_field(user_dao):
    first_user = valid_user(email="duplicate@example.com")

    second_user = {
        "firstName": "Bob",
        "lastName": "Berg",
        "email": "duplicate@example.com"
    }

    user_dao.create(first_user)

    with pytest.raises(WriteError):
        user_dao.create(second_user)
