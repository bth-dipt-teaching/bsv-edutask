import pytest
from unittest.mock import patch, MagicMock

# different systems under test
from src.util.daos import getDao
from src.util.helpers import diceroll
from src.controllers.usercontroller import UserController


class TestNamespaces:

    @pytest.mark.namespaces
    def test_1(self):

        # patch DAO in daos module
        with patch('src.util.daos.DAO') as mockedDAO:

            mock = MagicMock()

            mockedDAO.return_value = mock

            assert getDao(collection_name='test') == mock

    @pytest.mark.namespaces
    def test_2(self):

        # patch randint inside helpers module
        with patch('src.util.helpers.random.randint') as mockrandint:

            mockrandint.return_value = 6

            assert diceroll() == True

    @pytest.mark.namespaces
    def test_3(self):
        """
        Test get_user_by_email while mocking DAO and regex validation
        """

        user = {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'jane.doe'
        }

        # mock DAO
        mockedDAO = MagicMock()

        mockedDAO.find.return_value = [user]

        uc = UserController(dao=mockedDAO)

        # patch regex fullmatch
        with patch('re.fullmatch') as mockfullmatch:

            mockfullmatch.return_value = True

            assert uc.get_user_by_email(email='jane.doe') == user