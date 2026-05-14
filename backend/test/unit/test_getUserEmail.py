import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_service():
    return MagicMock()

@pytest.mark.unit
def test_get_valid_email(mock_service):

    mock_service.find.return_value = [{'email': 'test@gmail.com'}]
    user_controller = UserController(mock_service)
    result = user_controller.get_user_by_email('test@gmail.com')
    
    assert result == {'email': 'test@gmail.com'}
    
@pytest.mark.unit
def test_get_no_user_found(mock_service):
    
    mock_service.find.return_value = []
    user_controller = UserController(mock_service)
    result = user_controller.get_user_by_email('test@gmail.com')
    
    assert result is None
    
@pytest.mark.unit
def test_get_invalid_email(mock_service):
    with pytest.raises(ValueError):
        mock_service.find.return_value = [{'email': 'test.jakakkaaj'}]
        user_controller = UserController(mock_service)
        user_controller.get_user_by_email('testjakakkaaj')
        
@pytest.mark.unit
def test_get_database_error(mock_service):
    with pytest.raises(Exception):
        mock_service.find.side_effect = Exception

        user_controller = UserController(mock_service)
        user_controller.get_user_by_email('test@gmail.com')

@pytest.mark.unit
def test_get_multiple_users_same_email(mock_service):
    user = [{"id": 1, "email": 'test@gmail.com'}, {"id": 2, "email": 'test@gmail.com'}]
    mock_service.find.return_value = user
    user_controller = UserController(mock_service)
    result = user_controller.get_user_by_email('test@gmail.com')

    assert result == user[0]