import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO
from pymongo.errors import DuplicateKeyError, PyMongoError, WriteError

class TestDAOCreate:
    @pytest.fixture
    def setup_dao(self):
        dao = DAO("todo")
        dao.collection.delete_many({})  
        yield dao
        dao.collection.delete_many({})

    @pytest.mark.dao_create
    def test_insert_collection(self, setup_dao):
        doc = {"description": "test_collection", "done": False}
        result = setup_dao.create(doc)
        assert result is not None
        assert result["_id"] is not None
        assert result["description"] == doc["description"]
        assert result["done"] is False

    @pytest.mark.dao_create
    def test_insert_incorrect_doc(self, setup_dao):
        doc = {"not_description": "no_info"} 
        with pytest.raises(WriteError):
            setup_dao.create(doc)

    @pytest.mark.dao_create
    def test_insert_incorrect_data_type(self, setup_dao):
        doc = "insert string" 
        with pytest.raises(WriteError):
            setup_dao.create(doc)

    @pytest.fixture
    def setup_user_dao(self):
        dao = DAO("user")
        dao.collection.delete_many({})  
        yield dao
        dao.collection.delete_many({})

    @pytest.mark.dao_create
    def test_not_unique_item(self, setup_user_dao):
        user1 = {"firstName": "Anna",
                 "lastName": "Andersson",
                 "email": "test@email.com"
                 }
        user2 = {"firstName": "Anna",
                 "lastName": "Andersson",
                 "email": "test@email.com"
                 }
        setup_user_dao.create(user1)

        with pytest.raises(WriteError):
            setup_user_dao.create(user2)

    @pytest.mark.dao_create
    def test_not_bson_type(self, setup_user_dao):
        user = {"firstName": ["Anna"],
                 "lastName": "Andersson",
                 "email": "test@email.com"
                 }

        with pytest.raises(WriteError):
            setup_user_dao.create(user)
        
    @pytest.mark.dao_create
    def test_database_fail(self, setup_user_dao):
        user = {"firstName": ["Anna"],
                 "lastName": "Andersson",
                 "email": "test@email.com"
                 }
        setup_user_dao.collection.insert_one = MagicMock(
            side_effect=PyMongoError("Database down")
        )

        with pytest.raises(PyMongoError):
            setup_user_dao.create(user)
        