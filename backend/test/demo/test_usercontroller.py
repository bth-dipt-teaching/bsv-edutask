import pytest

from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

@pytest.fixture
#Mocking
def sut():
    mock_dao = MagicMock()
    controller = UserController(dao=mock_dao)

    return controller, mock_dao


#i) If the user is valid it should return exactly one user found 
def test_get_user_by_email_single_result(sut):
    controller, mock_dao = sut
    mock_dao.find.return_value = [{"email": "test@example.com", "name": "Alice"}]
    result = controller.get_user_by_email("test@example.com")
    assert result == {"email": "test@example.com", "name": "Alice"}


#ii) Email is valid but it is not associated to any user it must return none
def test_get_user_by_email_no_result(sut):
    controller, mock_dao = sut
    mock_dao.find.return_value = []
    result = controller.get_user_by_email("nobody@example.com")
    assert result is None


#iii) The email is valid but multiple users have been found should return first user
def test_get_user_by_email_multiple_results(sut):
    controller, mock_dao = sut

    user1 = {"email": "dup@example.com", "name": "Alice"}
    user2 = {"email": "dup@example.com", "name": "Bob"}
    mock_dao.find.return_value = [user1, user2]

    result = controller.get_user_by_email("dup@example.com")
    assert result == user1


#iv) Invalid email, should raise a ValueError
def test_get_user_by_email_invalid_email(sut):
    controller, mock_dao = sut
    with pytest.raises(ValueError):
        controller.get_user_by_email("notanemail")
    mock_dao.find.assert_not_called()


#v) Empty string should raise ValueError
def test_get_user_by_email_empty_string(sut):
    controller, mock_dao = sut

    with pytest.raises(ValueError):
        controller.get_user_by_email("")

    mock_dao.find.assert_not_called()