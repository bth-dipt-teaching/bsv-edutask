import os
from pathlib import Path
from unittest.mock import Mock

import pytest
import pymongo
from pymongo.errors import WriteError

from src.util.dao import DAO


BACKEND_DIR = Path(__file__).resolve().parents[2]

TODO_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["description"],
        "properties": {
            "description": {
                "bsonType": "string",
                "description": "the description of a todo must be determined",
                "uniqueItems": True,
            },
            "done": {
                "bsonType": "bool",
            },
        },
    },
}


@pytest.fixture(scope="session")
def mongo_test_url() -> str:
    """Return the MongoDB URL used only for integration tests."""
    return os.environ.get("MONGO_TEST_URL", "mongodb://localhost:27018")


@pytest.fixture(scope="session")
def mongo_client(mongo_test_url: str):
    """Create a client for the integration test MongoDB instance."""
    client = pymongo.MongoClient(mongo_test_url, serverSelectionTimeoutMS=3000)

    try:
        client.admin.command("ping")
    except Exception as exc:
        pytest.skip(
            f"MongoDB integration instance is unreachable at {mongo_test_url}: {exc}"
        )

    yield client
    client.close()


@pytest.fixture
def todo_validator_mock(monkeypatch: pytest.MonkeyPatch):
    """Mock the validator provider so DAO.create is tested against the database only."""
    mocked_get_validator = Mock(return_value=TODO_VALIDATOR)
    monkeypatch.setattr("src.util.dao.getValidator", mocked_get_validator)
    return mocked_get_validator


@pytest.fixture
def todo_dao(
    monkeypatch: pytest.MonkeyPatch,
    mongo_client,
    mongo_test_url: str,
    todo_validator_mock,
) -> DAO:
    """
    Provide an isolated DAO for the todo collection.

    The fixture uses a dedicated Mongo URL, mocks the validator lookup, and drops
    the collection before and after each test so production-like data is not touched.
    """
    monkeypatch.setenv("MONGO_URL", mongo_test_url)

    previous_cwd = Path.cwd()
    os.chdir(BACKEND_DIR)

    database = mongo_client.edutask
    database.drop_collection("todo")

    try:
        dao = DAO(collection_name="todo")
        todo_validator_mock.assert_called_once_with("todo")
        yield dao
    finally:
        database.drop_collection("todo")
        os.chdir(previous_cwd)


@pytest.mark.integration
def test_create_returns_inserted_todo(todo_dao):
    payload = {"description": "Write assignment report", "done": False}

    created = todo_dao.create(payload)

    assert created["description"] == payload["description"]
    assert created["done"] is payload["done"]
    assert "_id" in created
    assert "$oid" in created["_id"]


@pytest.mark.integration
def test_create_raises_when_required_description_is_missing(todo_dao):
    with pytest.raises(WriteError):
        todo_dao.create({"done": False})


@pytest.mark.integration
def test_create_raises_when_done_has_wrong_type(todo_dao):
    with pytest.raises(WriteError):
        todo_dao.create({"description": "Invalid done type", "done": "False"})


@pytest.mark.integration
@pytest.mark.xfail(
    reason=(
        "Seeded defect: `uniqueItems` in the validator does not enforce uniqueness "
        "for a scalar field across documents."
    ),
    strict=True,
)
def test_create_raises_for_duplicate_description(todo_dao):
    todo_dao.create({"description": "Duplicate me", "done": False})

    with pytest.raises(WriteError):
        todo_dao.create({"description": "Duplicate me", "done": True})
