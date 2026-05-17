import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO


# ─────────────────────────────────────────────
#  Fixture: isolated test collection with teardown
# ─────────────────────────────────────────────

@pytest.fixture
def test_dao():
    """
    Creates a DAO instance pointed at a test collection.
    The collection is dropped after every test so production
    data is never touched and tests remain independent.
    """
    dao = DAO("todo")
    dao.collection.create_index("description", unique=True)
    yield dao
    dao.drop()


# ─────────────────────────────────────────────
#  Test Cases
# ─────────────────────────────────────────────

def test_valid_insert(test_dao):
    # Test inserting a valid todo item
    todo = {"description": "Buy groceries", "done": False}
    result = test_dao.create(todo)
    assert result["description"] == "Buy groceries"
    assert result["done"] is False
    assert "_id" in result


def test_missing_field(test_dao):
    # Missing 'description' field, should fail
    incomplete = {"done": False}
    with pytest.raises(WriteError):
        test_dao.create(incomplete)


def test_wrong_type(test_dao):
    # 'done' should be a boolean, not a string
    invalid = {"description": "Wrong type", "done": "no"}
    with pytest.raises(WriteError):
        test_dao.create(invalid)


def test_duplicate(test_dao):
    # Two items with same description – unique index violation
    test_dao.create({"description": "Walk the dog", "done": False})
    with pytest.raises(WriteError):
        test_dao.create({"description": "Walk the dog", "done": False})


def test_extra_field(test_dao):
    # Adding a property not in the schema – should be accepted
    data = {"description": "Learn pytest", "done": False, "priority": "high"}
    result = test_dao.create(data)
    assert result["description"] == "Learn pytest"
    assert result["priority"] == "high"
    assert "_id" in result

def test_empty_field(test_dao):
    # 'description' is empty string, should fail
    invalid = {"description": "", "done": False}
    with pytest.raises(WriteError):
        test_dao.create(invalid)