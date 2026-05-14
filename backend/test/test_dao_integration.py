import pytest
from src.util.dao import DAO

class MockValidator:
    def validate(self, data):
        return True
        


class MockInsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class MockCollection:

    def __init__(self, mode="valid"):
        self.mode = mode

    def insert_one(self, data):
        if self.mode == "missing":
            raise Exception("Missing required field")

        if self.mode == "invalid_type":
            raise Exception("Invalid data type")

        if self.mode == "duplicate":
            raise Exception("Duplicate value")

        if self.mode == "db_fail":
            raise Exception("Database failure")

        return MockInsertResult("123")

    def find_one(self, query):
        return {
            "_id": "123",
            "email": "test@example.com"
        }


@pytest.fixture
def dao_valid():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("valid")
    dao.validator = MockValidator()
    return dao


@pytest.fixture
def dao_missing():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("missing")
    dao.validator = MockValidator()
    return dao


@pytest.fixture
def dao_invalid():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("invalid_type")
    dao.validator = MockValidator()
    return dao


@pytest.fixture
def dao_duplicate():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("duplicate")
    dao.validator = MockValidator()
    return dao


@pytest.fixture
def dao_fail():
    dao = DAO.__new__(DAO)
    dao.collection = MockCollection("db_fail")
    dao.validator = MockValidator()
    return dao


def test_create_valid(dao_valid):
    data = {"email": "test@example.com"}
    result = dao_valid.create(data)

    assert result["_id"] == "123"
    assert result["email"] == "test@example.com"


def test_create_missing_field(dao_missing):
    data = {}
    with pytest.raises(Exception):
        dao_missing.create(data)


def test_create_invalid_type(dao_invalid):
    data = {"email": 123}
    with pytest.raises(Exception):
        dao_invalid.create(data)


def test_create_duplicate(dao_duplicate):
    data = {"email": "test@example.com"}
    with pytest.raises(Exception):
        dao_duplicate.create(data)


def test_create_db_failure(dao_fail):
    data = {"email": "test@example.com"}
    with pytest.raises(Exception):
        dao_fail.create(data)

