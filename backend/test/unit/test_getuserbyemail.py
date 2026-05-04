import pytest
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

@pytest.fixture
def mock_dao():
    dao = MagicMock()
    return dao

@pytest.mark.parametrize('email, dao_return, expected', [
    ('test@unique.com', [{'email' : 'test@unique.com'}], {'email' : 'test@unique.com'}),
    ('test@duplicate.com', [{'email' : 'test@duplicate.com'}, {'email' : 'test@duplicate.com'}], {'email' : 'test@duplicate.com'}),
    ('test@unknown.com', [], None)
])
@pytest.mark.lab1
def test_get_user_valid_email_format(email, mock_dao, dao_return, expected):
    """ Input has valid email format - unique email, duplicate email, no match. """
    # Arrange
    mock_dao.find.return_value = dao_return
    user_controller = UserController(mock_dao)
    # Act
    result = user_controller.get_user_by_email(email)
    # Assert
    assert result == expected

@pytest.mark.parametrize('email', [
    'invalidemail',
    'a@b'
])
@pytest.mark.lab1
def test_get_user_invalid_email_format(mock_dao, email):
    """ Input has invalid email format - missing @, missing .com """
    # Arrange
    user_controller = UserController(mock_dao)
    # Act
    with pytest.raises(ValueError, match = 'Error: invalid email address'):
        user_controller.get_user_by_email(email)

@pytest.mark.lab1
def test_get_user_dao_failure(mock_dao):
    """ Database operation fail. """
    # Arrange
    email = 'test@example.com'
    mock_dao.find.side_effect = Exception('Database failure')
    user_controller = UserController(mock_dao)
    # Act
    with pytest.raises(Exception, match = 'Database failure'):
        user_controller.get_user_by_email(email)
