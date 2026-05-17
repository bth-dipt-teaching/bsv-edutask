import pytest # type: ignore
from unittest.mock import patch
from pymongo.errors import WriteError, DuplicateKeyError # type: ignore

from src.util.dao import DAO


TEST_COLLECTION = "test_task"

MOCK_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title"],
        "properties": {
            "title": {"bsonType": "string"},
            "description": {"bsonType": "string"}
        }
    }
}


@pytest.fixture
def task_dao():
    with patch("src.util.dao.getValidator", return_value=MOCK_VALIDATOR):
        dao = DAO(TEST_COLLECTION)
        dao.drop()

        dao = DAO(TEST_COLLECTION)
        dao.collection.create_index("title", unique=True)

        yield dao

        dao.drop()


@pytest.mark.integration
def test_create_valid_unique_document(task_dao):
    result = task_dao.create({
        "title": "task1",
        "description": "desc"
    })

    assert result["title"] == "task1"
    assert result["description"] == "desc"
    assert "_id" in result


@pytest.mark.integration
def test_create_duplicate_unique_field_fails(task_dao):
    task_dao.create({
        "title": "task1",
        "description": "desc"
    })

    with pytest.raises(DuplicateKeyError):
        task_dao.create({
            "title": "task1",
            "description": "another desc"
        })


@pytest.mark.integration
def test_create_invalid_data_type_fails(task_dao):
    with pytest.raises(WriteError):
        task_dao.create({
            "title": 123,
            "description": "desc"
        })


@pytest.mark.integration
def test_create_missing_optional_field_succeeds(task_dao):
    result = task_dao.create({
        "title": "task2"
    })

    assert result["title"] == "task2"
    assert "_id" in result


@pytest.mark.integration
def test_create_missing_required_field_fails(task_dao):
    with pytest.raises(WriteError):
        task_dao.create({
            "description": "desc"
        })