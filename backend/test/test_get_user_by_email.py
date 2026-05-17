import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

def test_get_user_by_email():
    mock_dao =MagicMock()
    mock_dao.find.return_value=[{"email":"test@email.com"}]

    usercontroller = UserController(mock_dao)
    result= usercontroller.get_user_by_email("test@email.com")
    assert result ["email"] == "test@email.com"

def test_invalid_mail():
    mock_dao=MagicMock()
    controller = UserController(mock_dao)

    with pytest.raises(ValueError):
        controller.get_user_by_email("Invalid mail")

def test_no_user():
    mock_dao=MagicMock()
    mock_dao.find.return_value= []
    controller =UserController(mock_dao)
    result=controller.get_user_by_email("test@email.com")
    assert result is None
