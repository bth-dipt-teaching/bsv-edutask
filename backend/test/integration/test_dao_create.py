#Integration tests for DAO.create() method.
import pytest
from pymongo.errors import WriteError


class TestDAOUserCreate:
    #Integration tests for DAO.create() with user collection.
    
    def test_user_create_valid(self, user_dao):
        """Valid: user with all required fields passes validation"""
        data = {
            "firstName": "Tarun",
            "lastName": "Bo",
            "email": "tarun.bo@example.com"
        }
        result = user_dao.create(data)
        assert result is not None
        assert result["firstName"] == "Tarun"
        assert result["lastName"] == "Bo"
        assert result["email"] == "tarun.bo@example.com"
        assert "_id" in result
    
    def test_user_missing_required_field(self, user_dao):
        """Invalid: missing required email field raises WriteError"""
        data = {
            "firstName": "John",
            "lastName": "Doe"
        }
        with pytest.raises(WriteError):
            user_dao.create(data)
    
    def test_user_wrong_type(self, user_dao):
        """Invalid: firstName with wrong type (int) raises WriteError"""
        data = {
            "firstName": 123,
            "lastName": "Doe",
            "email": "john@example.com"
        }
        with pytest.raises(WriteError):
            user_dao.create(data)
    
    def test_user_duplicate_email_constraint(self, user_dao):
        """Invalid: duplicate email violates uniqueness constraint"""
        user_dao.create({
            "firstName": "Tarun",
            "lastName": "Bo",
            "email": "shared@example.com"
        })
        with pytest.raises(WriteError):
            user_dao.create({
                "firstName": "Victor",
                "lastName": "Ti",
                "email": "shared@example.com"
            })



