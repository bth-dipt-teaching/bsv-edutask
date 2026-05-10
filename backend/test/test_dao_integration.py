#made by ajay
import os
import uuid
from unittest.mock import patch

import pytest
from pymongo.errors import WriteError

from src.util.dao import DAO


COLLECTION_NAME = "user"

# A minimal validator schema that mirrors the real user validator,
# used so the mocked getValidator returns something MongoDB can work with.
MOCK_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email", "tasks"],
        "properties": {
            "firstName": {"bsonType": "string"},
            "lastName":  {"bsonType": "string"},
            "email":     {"bsonType": "string"},
            "tasks":     {"bsonType": "array"},
        }
    }
}


@pytest.fixture
def dao():
    os.environ["MONGO_URL"] = "mongodb://localhost:27017"
    # Mock getValidator so the Validator file-system dependency cannot
    # cause accidental failures — the integration under test is
    # DAO.create() <-> MongoDB only.
    with patch("src.util.dao.getValidator", return_value=MOCK_VALIDATOR):
        dao_instance = DAO(COLLECTION_NAME)
    test_marker = f"integration-test-{uuid.uuid4()}"
    yield dao_instance, test_marker
    dao_instance.collection.delete_many({"test_marker": test_marker})


def make_valid_user(test_marker):
    unique_part = uuid.uuid4().hex
    return {
        "firstName": f"Integration{unique_part[:8]}",
        "lastName":  f"User{unique_part[8:16]}",
        "email":     f"integration-{unique_part}@example.com",
        "tasks":     [],
        "test_marker": test_marker,
    }


def test_create_valid_user_succeeds(dao):
    dao_instance, test_marker = dao
    valid_user = make_valid_user(test_marker)
    created_user = dao_instance.create(valid_user)
    assert created_user is not None
    assert "_id" in created_user
    assert created_user["firstName"] == valid_user["firstName"]
    assert created_user["lastName"]  == valid_user["lastName"]
    assert created_user["email"]     == valid_user["email"]
    saved_user = dao_instance.collection.find_one({"email": valid_user["email"]})
    assert saved_user is not None


def test_create_missing_required_email_fails(dao):
    dao_instance, test_marker = dao
    invalid_user = make_valid_user(test_marker)
    invalid_user.pop("email")
    with pytest.raises(WriteError):
        dao_instance.create(invalid_user)


def test_create_wrong_type_for_tasks_fails(dao):
    dao_instance, test_marker = dao
    invalid_user = make_valid_user(test_marker)
    invalid_user["tasks"] = "not-an-array"
    with pytest.raises(WriteError):
        dao_instance.create(invalid_user)


def test_create_duplicate_email_fails_if_email_is_unique(dao):
    dao_instance, test_marker = dao
    first_user = make_valid_user(test_marker)
    second_user = dict(first_user)
    second_user["firstName"] = "Duplicate"
    dao_instance.create(first_user)
    with pytest.raises(Exception):
        dao_instance.create(second_user)