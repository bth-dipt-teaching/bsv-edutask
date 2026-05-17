# Copy the clean version
import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO


@pytest.fixture
def test_dao():
    """Fixture that creates a DAO connected to the user collection in MongoDB."""
    dao = DAO(collection_name='user')
    # Cleanup: drop the collection before starting tests
    try:
        dao.drop()
    except:
        pass
    # Recreate the collection with validator
    dao = DAO(collection_name='user')
    yield dao
    # Cleanup: drop the collection after tests complete
    try:
        dao.drop()
    except:
        pass


class TestDAOCreate:
    """Integration tests for DAO.create() method."""

    def test_valid_user_creation(self, test_dao):
        """TC1: Valid user creation with all required fields."""
        data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "jane@example.com"
        }
        
        result = test_dao.create(data)
        
        assert result is not None
        assert result["firstName"] == "Jane"
        assert result["lastName"] == "Doe"
        assert result["email"] == "jane@example.com"
        assert "_id" in result

    def test_missing_firstname(self, test_dao):
        """TC2: Missing required field (firstName) should raise WriteError."""
        data = {
            "lastName": "Doe",
            "email": "jane@example.com"
        }
        
        with pytest.raises(WriteError):
            test_dao.create(data)

    def test_missing_email(self, test_dao):
        """TC3: Missing required field (email) should raise WriteError."""
        data = {
            "firstName": "Jane",
            "lastName": "Doe"
        }
        
        with pytest.raises(WriteError):
            test_dao.create(data)

    def test_invalid_firstname_type(self, test_dao):
        """TC4: Invalid data type (firstName as number) should raise WriteError."""
        data = {
            "firstName": 123,
            "lastName": "Doe",
            "email": "jane@example.com"
        }
        
        with pytest.raises(WriteError):
            test_dao.create(data)

    def test_multiple_missing_fields(self, test_dao):
        """TC5: Multiple missing required fields should raise WriteError."""
        data = {
            "firstName": "Jane"
        }
        
        with pytest.raises(WriteError):
            test_dao.create(data)