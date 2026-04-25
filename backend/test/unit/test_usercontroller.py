import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController



@pytest.fixture
def mock_dao():
    return MagicMock()


@pytest.fixture
def controller(mock_dao):
    return UserController(mock_dao)



@pytest.mark.unit
def test_single_user_found(controller, mock_dao):
    user = MagicMock()
    user.email = "test@example.com"

    mock_dao.find.return_value = [user]

    result = controller.get_user_by_email("test@example.com")

    assert result.email == "test@example.com"


@pytest.mark.unit
def test_multiple_users_found(controller, mock_dao, capfd):
    user1 = MagicMock()
    user1.email = "test@example.com"

    user2 = MagicMock()
    user2.email = "test@example.com"

    mock_dao.find.return_value = [user1, user2]

    result = controller.get_user_by_email("test@example.com")

    out, _ = capfd.readouterr()
    assert "more than one user" in out.lower()

    assert result == user1


@pytest.mark.unit
def test_no_user_found(controller, mock_dao):
    result = controller.get_user_by_email("test@example.com")
    assert result is None

    


@pytest.mark.unit
def test_invalid_email(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")


@pytest.mark.unit
def test_empty_email(controller):
    with pytest.raises(ValueError):
        controller.get_user_by_email("")


@pytest.mark.unit
def test_none_email(controller):
    
    with pytest.raises(ValueError):
        controller.get_user_by_email(None)


@pytest.mark.unit
def test_invalid_email_partial(controller):
    
    with pytest.raises(ValueError):
        controller.get_user_by_email("test@")