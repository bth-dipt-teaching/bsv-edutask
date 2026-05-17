"""
Pytest configuration and fixtures for integration tests.
Provides isolated MongoDB test database with validation.
"""
import os
import pytest
import pymongo
from dotenv import dotenv_values
from src.util.dao import DAO
from src.util.validators import getValidator


TEST_DB_NAME = "edutask_test"


@pytest.fixture(scope="session")
def mongo_url():
    """Get MongoDB URL from environment or .env file."""
    local_mongo_url = dotenv_values('.env').get('MONGO_URL')
    return os.environ.get('MONGO_URL', local_mongo_url) or 'mongodb://localhost:27017'


@pytest.fixture(scope="session")
def test_mongo_client(mongo_url):
    """Create a MongoDB client connected to test MongoDB instance."""
    client = pymongo.MongoClient(mongo_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def test_db(test_mongo_client):
    """Get test database and create collections with validators and unique indexes."""
    db = test_mongo_client[TEST_DB_NAME]
    
    if "user" not in db.list_collection_names():
        validator = getValidator("user")
        db.create_collection("user", validator=validator)
    
    # Create unique index for email
    db["user"].create_index("email", unique=True)
    
    yield db
    
    # Cleanup: drop entire test database after all tests
    test_mongo_client.drop_database(TEST_DB_NAME)

@pytest.fixture(autouse=True)
def clear_collections(test_db):
    """Clear test collection before and after each test to ensure isolation."""
    # Clear before test
    test_db["user"].delete_many({})
    
    yield
    
    # Clear after test
    test_db["user"].delete_many({})
@pytest.fixture
def user_dao(test_db):
    """DAO instance for user collection connected to test database."""
    dao = DAO('user')
    # Override collection to use test database instead of production
    dao.collection = test_db['user']
    return dao

