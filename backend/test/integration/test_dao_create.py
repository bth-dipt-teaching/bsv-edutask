import os
from unittest.mock import patch

import pytest
import pymongo
from bson import ObjectId

from src.util.dao import DAO


TEST_MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
TEST_COLLECTION = "dao_create_integration_test"
MOCKED_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object"
    }
}


@pytest.fixture
def mocked_validator():
    with patch("src.util.dao.getValidator", return_value=MOCKED_VALIDATOR) as mocked_get_validator:
        yield mocked_get_validator


@pytest.fixture
def dao(mocked_validator):
    previous_mongo_url = os.environ.get("MONGO_URL")
    os.environ["MONGO_URL"] = TEST_MONGO_URL

    client = pymongo.MongoClient(TEST_MONGO_URL)
    database = client.edutask

    if TEST_COLLECTION in database.list_collection_names():
        database.drop_collection(TEST_COLLECTION)

    dao = DAO(collection_name=TEST_COLLECTION)
    mocked_validator.assert_called_once_with(TEST_COLLECTION)

    yield dao

    dao.drop()
    client.close()

    if previous_mongo_url is None:
        os.environ.pop("MONGO_URL", None)
    else:
        os.environ["MONGO_URL"] = previous_mongo_url


def user_like_document():
    return {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": "alice@example.com"
    }


def test_create_document_through_dao(dao):
    created_document = dao.create(user_like_document())

    assert "_id" in created_document
    assert "$oid" in created_document["_id"]
    assert ObjectId.is_valid(created_document["_id"]["$oid"])

    assert created_document["firstName"] == "Alice"
    assert created_document["lastName"] == "Andersson"
    assert created_document["email"] == "alice@example.com"
