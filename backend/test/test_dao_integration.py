import os

import pytest
import pymongo
from bson.objectid import ObjectId
from pymongo.errors import WriteError

from src.util.dao import DAO


pytestmark = pytest.mark.integration


@pytest.fixture
def mongo_url(monkeypatch):
    """Use the test MongoDB instance, not production data."""
    url = os.getenv(
        "TEST_MONGO_URL",
        "mongodb://root:root@localhost:27017/?authSource=admin",
    )
    monkeypatch.setenv("MONGO_URL", url)
    return url


@pytest.fixture
def clean_user_collection(mongo_url):
    """Create a clean user collection before each test and remove it after."""
    client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")

    db = client.edutask
    db.drop_collection("user")

    yield

    db.drop_collection("user")
    client.close()


@pytest.fixture
def user_dao(clean_user_collection):
    return DAO("user")


def test_create_valid_user(user_dao):
    user = {
        "firstName": "Anna",
        "lastName": "Andersson",
        "email": "anna@example.com",
    }

    result = user_dao.create(user)

    assert result["firstName"] == "Anna"
    assert result["lastName"] == "Andersson"
    assert result["email"] == "anna@example.com"
    assert "_id" in result


def test_create_user_with_optional_tasks_array(user_dao):
    task_id = ObjectId()
    user = {
        "firstName": "Bo",
        "lastName": "Bengtsson",
        "email": "bo@example.com",
        "tasks": [task_id],
    }

    result = user_dao.create(user)

    assert result["tasks"][0]["$oid"] == str(task_id)


def test_create_user_missing_required_email_fails(user_dao):
    user = {
        "firstName": "Carl",
        "lastName": "Carlsson",
    }

    with pytest.raises(WriteError):
        user_dao.create(user)


def test_create_user_with_wrong_type_fails(user_dao):
    user = {
        "firstName": True,
        "lastName": "Dahl",
        "email": "dahl@example.com",
    }

    with pytest.raises(WriteError):
        user_dao.create(user)


def test_create_duplicate_email_fails(user_dao):
    user_1 = {
        "firstName": "Eva",
        "lastName": "Ek",
        "email": "same@example.com",
    }

    user_2 = {
        "firstName": "Erik",
        "lastName": "Ek",
        "email": "same@example.com",
    }

    user_dao.create(user_1)

    with pytest.raises(WriteError):
        user_dao.create(user_2)
