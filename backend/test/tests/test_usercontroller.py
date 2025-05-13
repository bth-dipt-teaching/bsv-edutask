import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController


def test_get_user_by_email_valid_unique():
    # Test if the function returns one user with an unique email.
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = [{"user": "A user"}]

    sut = UserController(dao=mockedDAO)

    result = sut.get_user_by_email(email="hi@hello.com")

    assert result == {"user": "A user"}


def test_get_user_by_email_valid_not_unique():
    # Test if the function returns one user with a not unique email. Should return the first user in the list.
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = [{"user": "Another user"}, {"user": "A user"}]

    sut = UserController(dao=mockedDAO)

    result = sut.get_user_by_email(email="hi@hello.com")

    assert result == {"user": "Another user"}


def test_get_user_by_email_valid_not_in_db():
    # Test if None is returned when an email is not in the database
    mockedDAO = mock.MagicMock()

    mockedDAO.find.return_value = []

    sut = UserController(dao=mockedDAO)

    result = sut.get_user_by_email(email="hi@hello.com")

    assert result == None


def test_get_user_by_email_invalid_email():
    # Assert that an invalid email raises a ValueError
    with pytest.raises(ValueError):
        mockedDAO = mock.MagicMock()

        mockedDAO.find.return_value = [{"user": "A user"}]

        sut = UserController(dao=mockedDAO)

        result = sut.get_user_by_email(email="hello.com")


def test_get_user_by_email_db_fail():
    # Test an Exception is raised if the database fails
    with pytest.raises(Exception):
        mockedDAO = mock.MagicMock()

        mockedDAO.find.return_value = None

        sut = UserController(dao=mockedDAO)

        result = sut.get_user_by_email(email="hi@hello.com")
