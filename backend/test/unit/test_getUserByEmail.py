import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def daoMock():
    mockedDao = mock.MagicMock()
    mocked = UserController(dao=mockedDao)
    return mocked


@pytest.mark.unit
def test_getUserByEmail_invalid_email(daoMock):

    with pytest.raises(ValueError):
        daoMock.get_user_by_email("user.com")

@pytest.mark.unit
def test_getUserByEmail_empty_email(daoMock):

    with pytest.raises(ValueError):
        daoMock.get_user_by_email("")

@pytest.mark.unit
def test_getUserByEmail_zero_users(daoMock, capsys):
    # Mock find user from dao - return empty list
    daoMock.dao.find.return_value = []

    res = daoMock.get_user_by_email("user@hotmail.com")

    assert res == None

@pytest.mark.unit
def test_getUserByEmail_zero_users_error_msg(daoMock, capsys):
    # Mock find user from dao - return empty list
    daoMock.dao.find.return_value = []

    daoMock.get_user_by_email("user@hotmail.com")

    # Check the print error message, capture with capsys
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Error: no user found'

@pytest.mark.unit
def test_getUserByEmail_valid_oneUser(daoMock):
    expected = {"email": "user@hotmail.com"}
    # Mock find user from dao
    daoMock.dao.find.return_value = [{"email": "user@hotmail.com"}]

    res = daoMock.get_user_by_email("user@hotmail.com")

    assert res == expected

@pytest.mark.unit
def test_getUserByEmail_valid_moreUsers(daoMock, capsys):
    expected = {"email": "user@hotmail.com"}
    # Mock find user from dao
    daoMock.dao.find.return_value = [{"email": "user@hotmail.com"}, {"email": "user@hotmail.com"}]

    res = daoMock.get_user_by_email("user@hotmail.com")

    assert res == expected

@pytest.mark.unit
def test_getUserByEmail_valid_moreUsers_error_msg(daoMock, capsys):
    # Mock find user from dao
    daoMock.dao.find.return_value = [{"email": "user@hotmail.com"}, {"email": "user@hotmail.com"}]

    daoMock.get_user_by_email("user@hotmail.com")

    # Check the print error message as well, capture with capsys
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Error: more than one user found with mail user@hotmail.com'


@pytest.mark.unit
def test_getUserByEmail_exception(daoMock):
    # Expect raising exception because of DB error, mock error with side_effect
    daoMock.dao.find.side_effect = Exception
    
    with pytest.raises(Exception):
        daoMock.get_user_by_email("user@hotmail.com")
        

    
    
    