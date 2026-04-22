from unittest.mock import patch, MagicMock

from src.util.helpers import ValidationHelper

from src.controllers.usercontroller import UserController

import pytest


class TestGetUserByEmail:
    """ Tests the get_user_by_email method of the UserController class. """

    users = [
                {'firstName': 'Jane', 'lastName': 'Doe', 'email': 'jane.doe'},
                {'firstName': 'John', 'lastName': 'Doe', 'email': 'jane.doe'}
            ]

    @pytest.mark.unit
    @pytest.mark.parametrize("valid_email, dao_users, expected", [
        (False, [], ValueError),
        (True, [], Exception)
    ])
    @patch('re.fullmatch', autospec=True)
    def test_get_user_by_email_raises_exception(self, mockedfullmatch, valid_email, dao_users, expected):
        mockedfullmatch.return_value = valid_email

        mockedDAO = MagicMock()
        mockedDAO.find.return_value = dao_users

        uc = UserController(dao=mockedDAO)

        with pytest.raises(expected):
            uc.get_user_by_email(email='jane.doe')


    @pytest.mark.unit
    @pytest.mark.parametrize("dao_users, expected", [
        (users[:1], users[0]),
        (users, users[0])
    ])
    @patch('re.fullmatch', autospec=True)
    def test_get_user_by_email_returns_object(self, mockedfullmatch, dao_users, expected):
        mockedfullmatch.return_value = True

        mockedDAO = MagicMock()
        mockedDAO.find.return_value = dao_users

        uc = UserController(dao=mockedDAO)

        assert uc.get_user_by_email(email='jane.doe') == expected
