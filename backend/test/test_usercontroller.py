import pytest
from unittest.mock import patch, MagicMock
from src.util.daos import getDao
from src.controllers.usercontroller import UserController as usercontroller

class TestEmailLogin:
    @pytest.fixture
    def database_mock():
        dao_mock = MagicMock()
        return dao_mock
    
    @pytest.fixture
    def user_controller_mock(database_mock):
        user_c = usercontroller(database_mock)
        return user_c
    
    @pytest.fixture
    def get_user_mock(email, user_controller_mock):
        user = user_controller_mock()
        user.get_user_by_email(email)
        return user
    

    @pytest.mark.usercontroller
    def test_email(self, get_user_mock, user_controller_mock ):
        user_c = user_controller_mock()
        
        test_user = [
            {"name": "user_one", "email": "test@email.com"},
        ]

        user_c.dao.find.return_value = test_user
        email = "test@email.com"

        assert get_user_mock(email) is test_user[0]

    def test_invalid_email(self, get_user_mock):
        email = "invalid.com"
     
        with pytest.raises(ValueError, match=f"invalid email address"):
            get_user_mock(email)

    @pytest.mark.usercontroller
    def test_no_user(self):
        user_c = user_controller_mock()

        test_user = []
        email = "test@email.com"
        user_c.dao.find.return_value = test_user
        result = user_c.get_user_by_email(email)
        assert result is None

    @pytest.mark.usercontroller
    def test_multiple_users(self, capsys):
        user_c = user_controller_mock()

        test_users = [
            {"name": "user_one", "email": "test@email.com"},
            {"name": "user_two", "email": "test@email.com"},
        ]

        user_c.dao.find.return_value = test_users
        result = user_c.get_user_by_email("test@email.com")
        captured = capsys.readouterr()

        assert result == test_users[0]
        assert "more than one user found" in captured.out.lower() 

    @pytest.mark.usercontroller
    def test_database_failure(self):
        dao_mock = MagicMock()
        dao_mock.find.side_effect = Exception("Db down")
        user_c = usercontroller(dao_mock)
        email = "test@email.com"
     
        with pytest.raises(Exception):
            user_c.get_user_by_email(email)
        
    @pytest.mark.usercontroller
    def test_empty_input(self):
        dao_mock = MagicMock()
        user_c = usercontroller(dao_mock)
        email = ""
     
        with pytest.raises(ValueError, match=f"invalid email address"):
            user_c.get_user_by_email(email)
