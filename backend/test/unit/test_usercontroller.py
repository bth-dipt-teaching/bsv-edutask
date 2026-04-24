"""
Contains unit tests for the UserController class.
"""
from unittest.mock import MagicMock

from src.controllers.usercontroller import UserController

import pytest


class TestGetUserByEmail:
    """ Tests the get_user_by_email method of the UserController class. """

    users = [
                {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'},
                {'firstName': 'John', 'lastName': 'Doe', 'email': 'jane.doe@gmail.com'}
            ]

    # email addresses from
    # https://codefool.tumblr.com/post/15288874550/list-of-valid-and-invalid-email-addresses
    @pytest.mark.unit
    @pytest.mark.parametrize("email", [
        (''),
        ('plainaddress'),
        ('#@%^%#$@#$@#.com'),
        ('@example.com'),
        ('Joe Smith <email@example.com>'),
        ('email.example.com'),
        ('email@example@example.com'),
        ('.email@example.com'),
        ('email.@example.com'),
        ('email..email@example.com'),
        ('あいうえお@example.com'),
        ('email@example.com (Joe Smith)'),
        ('email@example'),
        ('email@-example.com'),
        ('email@example.web'),
        ('email@111.222.333.44444'),
        ('email@example..com'),
        ('Abc..123@example.com'),
        (r'”(),:;<>[\]@example.com'),
        ('just”not”right@example.com'),
        (r'this\ is"really"not\allowed@example.com')
    ])
    def test_invalid_email_raises_valueerror(self, email):
        """
        Tests that the get_user_by_email method 
        raises ValueError when it is passed an invalid email.
        """

        mocked_dao = MagicMock()
        mocked_dao.find.return_value = [{'email': email}]

        uc = UserController(dao=mocked_dao)

        with pytest.raises(ValueError):
            uc.get_user_by_email(email=email)


    @pytest.mark.unit
    @pytest.mark.parametrize("email", [
        ('email@example.com'),
        ('firstname.lastname@example.com'),
        ('email@subdomain.example.com'),
        ('firstname+lastname@example.com'),
        ('email@123.123.123.123'),
        ('email@[123.123.123.123]'),
        ('"email"@example.com'),
        ('1234567890@example.com'),
        ('email@example-one.com'),
        ('_______@example.com'),
        ('email@example.name'),
        ('email@example.museum'),
        ('email@example.co.jp'),
        ('firstname-lastname@example.com'),
        (r'much.”more\ unusual”@example.com'),
        ('very.unusual.”@”.unusual.com@example.com'),
        (r'very.”(),:;<>[]”.VERY.”very@\\ "very”.unusual@strange.example.com')
    ])
    def test_valid_email_not_raises_valueerror(self, email):
        """
        Tests that the get_user_by_email method does not
        raise a ValueError when it is passed a valid email.
        """

        mocked_dao = MagicMock()
        mocked_dao.find.return_value = [{'email': email}]

        uc = UserController(dao=mocked_dao)
        try:
            uc.get_user_by_email(email=email)
        except ValueError:
            assert False, "RAISED EXCEPTION <class 'ValueError'>"


    @pytest.mark.unit
    def test_raises_exception_when_db_fails(self):
        """
        Tests that the get_user_by_email method
        raises Exception when the database operation fails.
        """

        mocked_dao = MagicMock()
        mocked_dao.find.return_value = Exception

        uc = UserController(dao=mocked_dao)

        with pytest.raises(Exception):
            uc.get_user_by_email(email='jane@doe.com')


    @pytest.mark.unit
    @pytest.mark.parametrize("dao_users, expected", [
        (users[:1], users[0]),
        (users, users[0]),
        ([], None)
    ])
    def test_returns_object(self, dao_users, expected):
        """ Tests that the get_user_by_email returns the right values. """

        mocked_dao = MagicMock()
        mocked_dao.find.return_value = dao_users

        uc = UserController(dao=mocked_dao)

        assert uc.get_user_by_email(email='jane.doe@gmail.com') == expected


    @pytest.mark.unit
    @pytest.mark.parametrize("dao_users, expected", [
        ([], False),
        ([{}], False),
        ([{}, {}], True)
    ])
    def test_warning_prints(self, capsys, dao_users, expected):
        """
        Tests that the multiple users warning is only 
        printed when the list of users has multiple values.
        """
        mocked_dao = MagicMock()
        mocked_dao.find.return_value = dao_users

        uc = UserController(dao=mocked_dao)
        uc.get_user_by_email(email='jane.doe@gmail.com')
        captured = capsys.readouterr()
        assert (captured.out == 'Error: more than one user found ' \
                'with mail jane.doe@gmail.com\n') == expected
