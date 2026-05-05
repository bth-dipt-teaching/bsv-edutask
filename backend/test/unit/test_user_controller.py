import pytest
from unittest.mock import MagicMock, patch
from src.controllers.usercontroller import UserController

@pytest.fixture
def dao_mock():
    return MagicMock()

@pytest.fixture
def user_controller(dao_mock):
    return UserController(dao_mock)

@pytest.mark.unit
def test_get_user_by_email_invalid(user_controller, dao_mock):
    #Arrange
    dao_mock.find.return_value = None
    #Act & Assert 
    with pytest.raises(ValueError):
        user_controller.get_user_by_email("Email")
        

@pytest.mark.unit
def test_get_user_by_email_valid_email_no_user(user_controller, dao_mock):
    # arrange
    dao_mock.find.return_value = [None]
    
    # act
    result = user_controller.get_user_by_email("email@example.com")

    # assert
    assert result is None
    
    
@pytest.mark.unit
def test_get_user_by_email_exception(user_controller, dao_mock):
    #Arrange
    dao_mock.find.side_effect=Exception("DB Failure")
    
    #Act & Assert 
    with pytest.raises(Exception):
        user_controller.get_user_by_email("email@example.com")

@pytest.mark.unit
def test_get_user_by_email_valid(user_controller, dao_mock):
    # arrange
    test_user = {"name": "FooBar"}
    
    dao_mock.find.return_value = [test_user]

    # act
    result = user_controller.get_user_by_email("email@example.com")

    # assert
    assert result == test_user
    
@pytest.mark.unit
def test_get_user_by_email_valid_multi(user_controller, dao_mock):
    # arrange
    test_user1 = {"name": "FooBar"}
    test_user2 = {"name": "BarFoo"}
    
    dao_mock.find.return_value = [test_user1, test_user2]

    # act
    with patch("src.controllers.usercontroller.print") as mock_print:
        result = user_controller.get_user_by_email("email@example.com")

        # assert
        mock_print.assert_called_once_with("Error: more than one user found with mail email@example.com")
        assert result == test_user1
        
