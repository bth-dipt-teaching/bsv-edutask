import pytest
from src.util.dao import DAO


# As testers, we viewed this as a fully testable NONE production database.
@pytest.fixture
def db_sut():
    database = DAO('user')

    database.collection.delete_many({})

    yield database

    database.collection.delete_many({})

# Test create document with a valid structure.
@pytest.mark.integration
def test_create_document_valid(db_sut):
    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        "email": "test@test.com"
    }

    result = db_sut.create(document)

    assert result is not None
    assert "_id" in result


# Missing required field, raise exception.
@pytest.mark.integration
def test_create_document_invalid(db_sut):
    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        # No email
    }
    
    with pytest.raises(Exception):
        db_sut.create(document)


# Testing wrong data format, integer instead of string as specified by validator
@pytest.mark.integration
def test_create_document_wrong_datatype(db_sut):
    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        "email": 757
    }
    
    with pytest.raises(Exception):
        db_sut.create(document)


# Test with optional task-list
@pytest.mark.integration
def test_create_document_optinal_taks(db_sut):
    document = {
        "firstName": "Testing",
        "lastName": "Testsson",
        "email": "test2@test.com",
        "tasks": []
    }

    result = db_sut.create(document)

    assert result is not None
    assert "_id" in result

# Test with optional task-list as wrong format.
@pytest.mark.integration
def test_create_document_optinal_taks_wrong(db_sut):
    document = {
        "firstName": "A",
        "lastName": "B",
        "email": "a@test.com",
        "tasks": ["wrong"]
    }

    with pytest.raises(Exception):
        db_sut.create(document)


@pytest.mark.integration
def test_create_document_empty(db_sut):
    with pytest.raises(Exception):
        db_sut.create({})