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
    def valid_email():
        return "test@email.com"
    

    @pytest.mark.usercontroller
    def test_email(self, user_controller_mock, valid_email):
        
        test_user = [
            {"name": "user_one", "email": "test@email.com"},
        ]
   
        user_controller_mock.dao.find.return_value = test_user

        result = user_controller_mock.get_user_by_email(valid_email)
        
        assert result == test_user[0]
        assert result["email"] == test_user[0]["email"]

    def test_invalid_email(self, get_user_mock):
        email = "invalid.com"
     
        with pytest.raises(ValueError, match=f"invalid email address"):
            get_user_mock(email)

    @pytest.mark.usercontroller
    def test_no_user(self, user_controller_mock ,valid_email):
        test_user = []
        user_controller_mock.dao.find.return_value = test_user
        result = user_controller_mock.get_user_by_email(valid_email)
        assert result is None

    @pytest.mark.usercontroller
    def test_multiple_users(self, capsys, user_controller_mock, valid_email):

        test_users = [
            {"name": "user_one", "email": "test@email.com"},
            {"name": "user_two", "email": "test@email.com"},
        ]

        user_controller_mock.dao.find.return_value = test_users
        result = user_controller_mock.get_user_by_email(valid_email)
        captured = capsys.readouterr()

        assert result == test_users[0]
        assert "more than one user found" in captured.out.lower() 

    @pytest.mark.usercontroller
    def test_database_failure(self, valid_email):
        dao_mock = MagicMock()
        dao_mock.find.side_effect = Exception("Db down")
        user_c = usercontroller(dao_mock)
     
        with pytest.raises(Exception):
            user_c.get_user_by_email(valid_email)
        
    @pytest.mark.usercontroller
    def test_empty_input(self, user_controller_mock):
        with pytest.raises(ValueError, match=f"invalid email address"):
            user_controller_mock.get_user_by_email("")
