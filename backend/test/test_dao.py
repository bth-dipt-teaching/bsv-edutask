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


