import pytest  # type: ignore
from src.util.daos import getDao


# ---------------- FIXTURES ----------------

@pytest.fixture
def task_dao():
    dao = getDao("task")
    dao.drop()
    yield dao
    dao.drop()


@pytest.fixture
def video_dao():
    dao = getDao("video")
    dao.drop()
    yield dao
    dao.drop()


@pytest.fixture
def todo_dao():
    dao = getDao("todo")
    dao.drop()
    yield dao
    dao.drop()


# ---------------- TASK TESTS ----------------

@pytest.mark.integration
def test_create_task_valid(task_dao):
    data = {
        "title": "task1",
        "description": "desc"
    }

    result = task_dao.create(data)

    assert result["title"] == "task1"
    assert result["description"] == "desc"
    assert "_id" in result


@pytest.mark.integration
def test_create_task_missing_title(task_dao):
    data = {
        "description": "desc"
    }

    with pytest.raises(Exception):
        task_dao.create(data)


@pytest.mark.integration
def test_create_task_title_not_string(task_dao):
    data = {
        "title": 123,
        "description": "desc"
    }

    with pytest.raises(Exception):
        task_dao.create(data)


@pytest.mark.integration
def test_create_task_startdate_not_date(task_dao):
    data = {
        "title": "task2",
        "description": "desc",
        "startdate": "today"
    }

    with pytest.raises(Exception):
        task_dao.create(data)


@pytest.mark.integration
def test_create_task_video_not_objectid(task_dao):
    data = {
        "title": "task3",
        "description": "desc",
        "video": "not_an_objectid"
    }

    with pytest.raises(Exception):
        task_dao.create(data)


# ---------------- VIDEO TESTS ----------------

@pytest.mark.integration
def test_create_video_valid(video_dao):
    data = {
        "url": "www.test.com"
    }

    result = video_dao.create(data)

    assert result["url"] == "www.test.com"
    assert "_id" in result


@pytest.mark.integration
def test_create_video_invalid_type(video_dao):
    data = {
        "url": 123
    }

    with pytest.raises(Exception):
        video_dao.create(data)


# ---------------- TODO TESTS ----------------

@pytest.mark.integration
def test_create_todo_valid(todo_dao):
    data = {
        "description": "todo item",
        "done": False
    }

    result = todo_dao.create(data)

    assert result["description"] == "todo item"
    assert result["done"] is False
    assert "_id" in result


@pytest.mark.integration
def test_create_todo_done_not_bool(todo_dao):
    data = {
        "description": "todo item",
        "done": "False"
    }

    with pytest.raises(Exception):
        todo_dao.create(data)