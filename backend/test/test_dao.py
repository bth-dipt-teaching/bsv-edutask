import pytest
import os
from pymongo import MongoClient
from src.util.dao import DAO

# ✅ FIX: force correct working directory
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# -----------------------
# FIXTURES
# -----------------------

@pytest.fixture
def collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["edutask_test"]

    # Drop collection first (important)
    db.drop_collection("user")

    # Create collection with validator
    db.create_collection("user", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["firstName", "lastName", "email"],
            "properties": {
                "firstName": {"bsonType": "string"},
                "lastName": {"bsonType": "string"},
                "email": {"bsonType": "string"}
            }
        }
    })

    col = db["user"]

    # Optional: enforce unique email
    col.create_index("email", unique=True)

    return col


@pytest.fixture
def dao(collection):
    dao = DAO("user")  # must match user.json
    dao.collection = collection
    return dao

# -----------------------
# TEST CASES 
# -----------------------

def test_valid_user(dao):
    data = {
        "firstName": "Ibbu",
        "lastName": "Khan",
        "email": "ibbu@example.com"
    }

    result = dao.create(data)
    assert result is not None


def test_missing_required_field(dao):
    data = {
        "firstName": "Abhi",
        # missing lastName
        "email": "abhi@example.com"
    }

    with pytest.raises(Exception):
        dao.create(data)


def test_wrong_data_type(dao):
    data = {
        "firstName": 123,  # should be string
        "lastName": "Rahul",
        "email": "rahul@example.com"
    }

    with pytest.raises(Exception):
        dao.create(data)


def test_duplicate_email(dao):
    data = {
        "firstName": "Sameen",
        "lastName": "Ali",
        "email": "sameen@example.com"
    }

    dao.create(data)

    # duplicate insert
    with pytest.raises(Exception):
        dao.create(data)


def test_created_document_has_id(dao):
    data = {
        "firstName": "Rahul",
        "lastName": "Sharma",
        "email": "rahul.sharma@example.com"
    }

    result = dao.create(data)

    assert "_id" in result


