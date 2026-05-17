import pytest
import pytest
pytestmark = pytest.mark.integration
from datetime import datetime
import uuid

from src.util.dao import DAO

pytestmark = pytest.mark.integration


@pytest.fixture
def dao_instance():
    dao = DAO("task")
    yield dao
    dao.drop()


def generate_data():
    return {
        "title": f"task-{uuid.uuid4()}",
        "description": "integration test"
    }

def test_create_success(dao_instance):
    data = generate_data()
    result = dao_instance.create(data)

    assert "_id" in result


def test_create_missing_title(dao_instance):
    data = {"description": "missing title"}

    with pytest.raises(Exception):
        dao_instance.create(data)


def test_create_invalid_type(dao_instance):
    data = {
        "title": 123,
        "description": "invalid type"
    }

    with pytest.raises(Exception):
        dao_instance.create(data)


def test_create_with_extra_fields(dao_instance):
    data = {
        "title": f"task-{uuid.uuid4()}",
        "description": "extra",
        "categories": ["x", "y"],
        "startdate": datetime.now()
    }

    result = dao_instance.create(data)

    assert result["categories"] == ["x", "y"]


def test_create_invalid_categories(dao_instance):
    data = {
        "title": f"task-{uuid.uuid4()}",
        "description": "bad",
        "categories": "wrong"
    }

    with pytest.raises(Exception):
        dao_instance.create(data)


def test_create_empty_description(dao_instance):
    data = {
        "title": f"task-{uuid.uuid4()}",
        "description": ""
    }

    result = dao_instance.create(data)
    assert result["_id"] is not None
    