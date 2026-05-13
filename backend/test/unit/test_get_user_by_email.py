import pytest
from unittest import mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    return mock.MagicMock()

@pytest.mark.unit
class TestGetUserByEmail:

    # The following two test functions (single_valid and multiple_valid) test similar scenarios
    # and could potentially be combined into one parameterized test using @pytest.mark.parametrize.
    # However, they are kept separate here for clarity and readability.
    def test_get_user_email_single_valid(self, mock_dao):
        #Arrange
        #Create a fake user that the mock database will return
        fake_user = {"_id": "abc123", "email": "single.user@example.com", "name": "Kalle"}
        mock_dao.find.return_value = [fake_user]
        user_controller = UserController(mock_dao)
        email = "single.user@example.com"
        #Act
        result = user_controller.get_user_by_email(email)
        #Assert
        assert result == fake_user
    
    def test_get_user_email_multiple_valid(self, mock_dao):
        #Arrange
        #Create two fake users with the same email (duplicate)
        fake_user_1 = {"_id": "id1", "email": "dup@example.com", "name": "Alex"}
        fake_user_2 = {"_id": "id2", "email": "dup@example.com", "name": "Charlie"}
        mock_dao.find.return_value = [fake_user_1, fake_user_2]
        user_controller = UserController(mock_dao)
        email = "dup@example.com"
        #Act
        result = user_controller.get_user_by_email(email)
        #Assert
        #According to the docstring, the first user should be returned when there are multiple
        assert result == fake_user_1
    
    
    @pytest.mark.parametrize("input", [
        ("invalid_email"),
        (None) #Assumes 
    ])
    def test_get_user_email_invalid_email(self, mock_dao, input):
        #Arrange
        user_controller = UserController(mock_dao)
        #Act
        #Assert
        with pytest.raises(ValueError):
            user_controller.get_user_by_email(input)
       
    
    def test_get_user_email_database_error(self, mock_dao):
        #Arrange
        #use of side_effect found in the unittest.mock documentation
        #"side_effect
        # This can either be a function to be called when the mock is called, an iterable or an exception (class or instance) to be raised."
        mock_dao.find.side_effect = Exception("[Error] Database crached")
        user_controller = UserController(mock_dao)
        email = "valid.test@email.com"
        #Act
        #Assert
        with pytest.raises(Exception):
            user_controller.get_user_by_email(email)
        
    
  
    def test_get_user_email_no_user(self, mock_dao):
        """
            Function test behaviour of when there is no user for the given email.
            Expected result is None, as defined in the method doc text.
            Test fails because currently it always returns the first item when the length is not 1.
            I.e. raises an index error, instead of returning None.
        """
        #Arrange
        mock_dao.find.return_value = []
        user_controller = UserController(mock_dao)
        valid_email = "user.test@fakeuser.com"
        #Act
        res = user_controller.get_user_by_email(valid_email)
        #Assert
        assert res == None
