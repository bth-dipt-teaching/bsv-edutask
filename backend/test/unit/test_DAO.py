import pytest
from pymongo import MongoClient
from src.util.dao import DAO

from unittest.mock import MagicMock


@pytest.fixture
def create_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test"]

    yield db

    client.drop_database("test")


def test_create_valid(create_db):
    dao = DAO("task")

    dao.db = create_db
    dao.collection = create_db["task"]

    data = {
        "name": "Test",
        "description": "lieuhipuegah"
    }

    dao.create(data)

    result = create_db["task"].find_one({"name": "Test"})
    assert result is not None
    
def test_create_data_not_dict(create_db):
    dao = DAO("task")
    dao.db = create_db
    dao.collection = create_db["task"]

    data = 1

    with pytest.raises(Exception):
        dao.create(data)
        
def test_create_with_diffrent_datatypes_in_dict(create_db):
    dao = DAO("task")
    dao.db = create_db
    dao.collection = create_db["task"]

    data = {"invalid": "data", "name": "Test", "number": 123, "list": [1, 2, 3], "dict": {"key": "value"}}

    dao.create(data)

    result = create_db["task"].find_one({"name": "Test"})
    assert result is not None
    
def test_database_invalid_values(create_db):
    dao = DAO("task")
    dao.collection = MagicMock()
    data = 1
    with pytest.raises(Exception):
        dao.create(data)
        
def test_create_with_empty_dict():
    dao = DAO("task")
    dao.collection = MagicMock()
    data = {}
    with pytest.raises(Exception):
        dao.create(data)
    
def test_create_duplicated_dict(create_db):
    
    dao = DAO("task")
    dao.db = create_db
    dao.collection = create_db["task"]
    data = {
        "name": "Test",
        "description": "lieuhipuegah"
    }
    
    data2 = {
        "name": "Test",
        "description": "iuheiuabe"
    }

    dao.create(data)
    dao.create(data2)
    

    result = create_db["task"].find_one({"name": "Test"})
    assert result is not None
    
def test_create_mongo_exception_error():
    dao = DAO("task")
    dao.collection = MagicMock()

    dao.collection.insert_one.side_effect = Exception("Error")

    with pytest.raises(Exception):
        dao.create({"name": "Test"})
    
