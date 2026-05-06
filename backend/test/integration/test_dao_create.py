from unittest.mock import patch

import pytest
from bson.objectid import ObjectId
from pymongo.errors import WriteError

from src.util.dao import DAO


VALIDATORS = {
    "task": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "description"],
            "properties": {
                "title": {
                    "bsonType": "string",
                    "description": "the title of a task must be determined",
                    "uniqueItems": True
                },
                "description": {
                    "bsonType": "string",
                    "description": "the description of a task must be determined"
                },
                "startdate": {
                    "bsonType": "date"
                },
                "duedate": {
                    "bsonType": "date"
                },
                "requires": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"
                    }
                },
                "categories": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string"
                    }
                },
                "todos": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"
                    }
                },
                "video": {
                    "bsonType": "objectId"
                }
            }
        }
    },
    "todo": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["description"],
            "properties": {
                "description": {
                    "bsonType": "string",
                    "description": "the description of a todo must be determined",
                    "uniqueItems": True
                },
                "done": {
                    "bsonType": "bool"
                }
            }
        }
    },
    "user": {
        "$jsonSchema": {
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
    },
    "video": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["url"],
            "properties": {
                "url": {
                    "bsonType": "string",
                    "description": "the url of a YouTube video must be determined"
                }
            }
        }
    }
}


@pytest.fixture
def dao_factory():
    created_daos = []

    def _create_dao(collection_name):
        with patch("src.util.dao.getValidator", return_value=VALIDATORS[collection_name]):
            dao = DAO(collection_name)
            dao.drop()

            dao = DAO(collection_name)
            created_daos.append(dao)

            return dao

    yield _create_dao

    for dao in created_daos:
        dao.drop()

# --------------------
# task.json tests
# --------------------

def test_create_valid_task_succeeds(dao_factory):
    dao = dao_factory("task")

    data = {
        "title": "Test task",
        "description": "This is a valid task"
    }

    result = dao.create(data)

    assert result is not None
    assert "_id" in result
    assert result["title"] == "Test task"
    assert result["description"] == "This is a valid task"


def test_create_task_missing_title_fails(dao_factory):
    dao = dao_factory("task")

    data = {
        "description": "Missing title"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_task_missing_description_fails(dao_factory):
    dao = dao_factory("task")

    data = {
        "title": "Missing description"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_task_wrong_title_type_fails(dao_factory):
    dao = dao_factory("task")

    data = {
        "title": 123,
        "description": "Title must be a string"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_task_valid_categories_succeeds(dao_factory):
    dao = dao_factory("task")

    data = {
        "title": "Task with categories",
        "description": "Categories are valid",
        "categories": ["school", "testing"]
    }

    result = dao.create(data)

    assert result["categories"] == ["school", "testing"]


def test_create_task_wrong_categories_type_fails(dao_factory):
    dao = dao_factory("task")

    data = {
        "title": "Wrong categories",
        "description": "Categories must be an array",
        "categories": "school"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_task_valid_objectid_fields_succeeds(dao_factory):
    dao = dao_factory("task")

    todo_id = ObjectId()
    video_id = ObjectId()

    data = {
        "title": "Task with references",
        "description": "ObjectId references are valid",
        "todos": [todo_id],
        "video": video_id
    }

    result = dao.create(data)

    assert result["title"] == "Task with references"
    assert result["todos"][0]["$oid"] == str(todo_id)
    assert result["video"]["$oid"] == str(video_id)


# --------------------
# todo.json tests
# --------------------

def test_create_valid_todo_succeeds(dao_factory):
    dao = dao_factory("todo")

    data = {
        "description": "This is a valid todo",
        "done": False
    }

    result = dao.create(data)

    assert result is not None
    assert "_id" in result
    assert result["description"] == "This is a valid todo"
    assert result["done"] is False


def test_create_todo_missing_description_fails(dao_factory):
    dao = dao_factory("todo")

    data = {
        "done": False
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_todo_wrong_description_type_fails(dao_factory):
    dao = dao_factory("todo")

    data = {
        "description": 123,
        "done": False
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_todo_wrong_done_type_fails(dao_factory):
    dao = dao_factory("todo")

    data = {
        "description": "Wrong done type",
        "done": "false"
    }

    with pytest.raises(WriteError):
        dao.create(data)


# --------------------
# user.json tests
# --------------------

def test_create_valid_user_succeeds(dao_factory):
    dao = dao_factory("user")

    data = {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": "alice@example.com"
    }

    result = dao.create(data)

    assert result is not None
    assert "_id" in result
    assert result["firstName"] == "Alice"
    assert result["lastName"] == "Andersson"
    assert result["email"] == "alice@example.com"


def test_create_user_missing_first_name_fails(dao_factory):
    dao = dao_factory("user")

    data = {
        "lastName": "Andersson",
        "email": "alice@example.com"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_user_missing_last_name_fails(dao_factory):
    dao = dao_factory("user")

    data = {
        "firstName": "Alice",
        "email": "alice@example.com"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_user_missing_email_fails(dao_factory):
    dao = dao_factory("user")

    data = {
        "firstName": "Alice",
        "lastName": "Andersson"
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_user_wrong_email_type_fails(dao_factory):
    dao = dao_factory("user")

    data = {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": 123
    }

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_user_valid_tasks_array_succeeds(dao_factory):
    dao = dao_factory("user")

    task_id = ObjectId()

    data = {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": "alice@example.com",
        "tasks": [task_id]
    }

    result = dao.create(data)

    assert result["tasks"][0]["$oid"] == str(task_id)


def test_create_user_wrong_tasks_type_fails(dao_factory):
    dao = dao_factory("user")

    data = {
        "firstName": "Alice",
        "lastName": "Andersson",
        "email": "alice@example.com",
        "tasks": "not an array"
    }

    with pytest.raises(WriteError):
        dao.create(data)


# --------------------
# video.json tests
# --------------------

def test_create_valid_video_succeeds(dao_factory):
    dao = dao_factory("video")

    data = {
        "url": "https://www.youtube.com/watch?v=test"
    }

    result = dao.create(data)

    assert result is not None
    assert "_id" in result
    assert result["url"] == "https://www.youtube.com/watch?v=test"


def test_create_video_missing_url_fails(dao_factory):
    dao = dao_factory("video")

    data = {}

    with pytest.raises(WriteError):
        dao.create(data)


def test_create_video_wrong_url_type_fails(dao_factory):
    dao = dao_factory("video")

    data = {
        "url": 123
    }

    with pytest.raises(WriteError):
        dao.create(data)