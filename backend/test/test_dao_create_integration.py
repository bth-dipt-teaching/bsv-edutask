import pytest
import json
from pathlib import Path

from pymongo import MongoClient

from src.util.dao import DAO


@pytest.fixture(scope="module")
def mongo_test_db():
    """Create a test-only Mongo collection and return a DAO bound to it."""
    client = MongoClient("mongodb://root:root@localhost:27017")

    db = client["edutask_test"]
    collection_name = "it_user_create"
    
    validator_path = Path(__file__).resolve().parents[1] / "src" / "static" / "validators" / "user.json"
    # this specific row was from LLM, but it is needed to load the validator anywhere

    with open(validator_path, "r") as validator_file:
        validator = json.load(validator_file)

    if collection_name in db.list_collection_names():
        db[collection_name].drop()
    db.create_collection(collection_name, validator=validator)

    dao = DAO.__new__(DAO)
    dao.collection = db[collection_name]

    try:
        yield dao
    finally:
        db[collection_name].drop()
        client.close()


def test_create_valid_document(mongo_test_db):
    """Should insert a valid document and return the created object."""
    data = {
        "firstName": "Ardian",
        "lastName": "Qeriqi",
        "email": "ardian@example.com"
    }

    created = mongo_test_db.create(data)

    assert created["firstName"] == "Ardian"
    assert created["lastName"] == "Qeriqi"
    assert created["email"] == "ardian@example.com"
    assert "_id" in created


def test_create_invalid_document_rejected(mongo_test_db):
    """Should reject invalid data that violates the collection validator."""
    invalid_data = {
        "firstName": "Habibullah",
        "lastName": "Amin"
    }

    with pytest.raises(Exception):
        mongo_test_db.create(invalid_data)
