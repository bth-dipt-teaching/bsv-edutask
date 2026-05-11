import pytest # type: ignore
from unittest.mock import patch
from pymongo.errors import WriteError # type: ignore

from src.util.dao import DAO


MOCK_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title"],
        "properties": {
            "title": {
                "bsonType": "string"
            },
            "done": {
                "bsonType": "bool"
            }
        }
    }
}


@pytest.fixture
def task_dao():
    with patch("src.util.dao.getValidator", return_value=MOCK_VALIDATOR):
        dao = DAO("task")
        dao.drop()

        dao = DAO("task")

        yield dao

        dao.drop()


@pytest.mark.integration
def test_create_valid_document(task_dao):
    data = {
        "title": "task1",
        "done": False
    }

    result = task_dao.create(data)

    assert result["title"] == "task1"
    assert result["done"] is False
    assert "_id" in result


@pytest.mark.integration
def test_create_returns_created_object_with_id(task_dao):
    data = {
        "title": "task2"
    }

    result = task_dao.create(data)

    assert result["title"] == "task2"
    assert "_id" in result
    assert "$oid" in result["_id"]


@pytest.mark.integration
def test_create_document_is_saved_in_database(task_dao):
    created = task_dao.create({
        "title": "task3",
        "done": True
    })

    found = task_dao.findOne(created["_id"]["$oid"])

    assert found["title"] == "task3"
    assert found["done"] is True
    assert found["_id"] == created["_id"]


@pytest.mark.integration
def test_create_missing_required_field_fails(task_dao):
    data = {
        "done": False
    }

    with pytest.raises(WriteError):
        task_dao.create(data)


@pytest.mark.integration
def test_create_wrong_field_type_fails(task_dao):
    data = {
        "title": 123,
        "done": False
    }

    with pytest.raises(WriteError):
        task_dao.create(data)


@pytest.mark.integration
def test_create_optional_field_wrong_type_fails(task_dao):
    data = {
        "title": "task4",
        "done": "False"
    }

    with pytest.raises(WriteError):
        task_dao.create(data)


@pytest.mark.integration
def test_create_multiple_valid_documents(task_dao):
    task_dao.create({"title": "task1"})
    task_dao.create({"title": "task2", "done": True})

    results = task_dao.find()

    assert len(results) == 2

    titles = [task["title"] for task in results]

    assert "task1" in titles
    assert "task2" in titles