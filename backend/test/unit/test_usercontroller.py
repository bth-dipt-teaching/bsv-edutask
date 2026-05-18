import pytest
import unittest.mock as mock 


from src.controllers.usercontroller import UserController

@pytest.fixture
def sut(daoList):
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = daoList

    mockedReturnValue = UserController(dao=mockedDAO)
    return mockedReturnValue

"""test if the first object is returned if email is calid and None is returned if email is valid but not in Database"""

@pytest.mark.unit
@pytest.mark.parametrize('daoList, expected',
    [
        ([{"email": 'viktor@gmail.com'}], {"email": 'viktor@gmail.com'}),
        ([{"email": 'viktor@gmail.com'}, {"email": 'viktor@gmail.com'}, {"email": 'viktor@gmail.com'}], {"email": 'viktor@gmail.com'}),
        ([], None)
    ]
)

def test_valid_email(sut, expected):
    ValidEmailResult = sut.get_user_by_email(email = "viktor@gmail.com")

    assert ValidEmailResult == expected

"""test if Value Error is thrown if email is not valid"""
@pytest.mark.unit
@pytest.mark.parametrize('daoList, expected',
    [
        ([{"email": 'viktor@gmail.com'}], {"email": 'viktor@gmail.com'}),
    ]
)
def test_invalid_email(sut, expected):
    with pytest.raises(ValueError):
        InvalidEmailResult = sut.get_user_by_email(email="asdfghjkl")

        assert InvalidEmailResult == expected

"""test if Exception is thrown if database error"""
@pytest.mark.unit
def test_database_error():
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = Exception

    mockedReturnValue = UserController(dao=mockedDAO)

    with pytest.raises(Exception):
        expected = {"email": 'viktor@gmail.com'}
        databaseErrorResult = mockedReturnValue.get_user_by_email(email='viktor@gmail.com')

        assert databaseErrorResult == expected

"""Extra test for checking if the print statement when in side the else statement (a whiteboc test)"""
@pytest.mark.unit
def test_Usercontroller_multipleUsers(capsys):
    mockedDao = mock.MagicMock()

    mockedDao.find.return_value = [{'email': 'viktor@gmail.com'}, {'email': 'viktor@gmail.com'}, {'email': 'viktor@gmail.com'}]

    mockedUser = UserController(dao=mockedDao)

    mockedUser.get_user_by_email(email='viktor@gmail.com')
    captured_print = capsys.readouterr()
    assert captured_print.out == 'Error: more than one user found with mail viktor@gmail.com\n'