from unittest.mock import MagicMock
import pytest
from src.controllers.usercontroller import UserController

class TestGetUserByEmail:
    """
    Unit tests for get_user_by_email in UserController.
    
    Oracle: The docstring/specification of the function.
    
    Test cases derived using the 4-step test design technique:
    
    Conditions:
        C1: Email format is valid (Yes / No)
        C2: Number of users found (0 / 1 / More than 1)
        C3: Database operation succeeds (Yes / No)
    
    Valid combinations:
        TC1: C1=No  -> ValueError raised
        TC2: C1=Yes, C2=0,  C3=Yes -> None returned
        TC3: C1=Yes, C2=1,  C3=Yes -> User object returned
        TC4: C1=Yes, C2=>1, C3=Yes -> First user returned + warning printed
        TC5: C1=Yes, C2=—,  C3=No  -> Exception raised
    
    Note: TC2 is expected to fail due to a bug in the implementation.
    When no user is found, the code calls users[0] on an empty list,
    causing an IndexError instead of returning None as specified.
    """

    # TC1: Invalid email format -> ValueError raised
    def test_invalid_email(self):
        # Arrange
        mock_dao = MagicMock()
        controller = UserController(dao=mock_dao)

        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            controller.get_user_by_email("userexample.com")
        assert str(excinfo.value) == 'Error: invalid email address'

    # TC2: 0 users found -> None returned
    # NOTE: Expected to fail due to bug — code does users[0] on empty list
    def test_no_user_found(self):
        # Arrange
        mock_dao = MagicMock()
        mock_dao.find.return_value = []
        controller = UserController(dao=mock_dao)

        # Act
        result = controller.get_user_by_email("nonexistent@example.com")

        # Assert
        assert result is None

    # TC3: 1 user found -> User object returned
    def test_one_user_found(self):
        # Arrange
        mock_dao = MagicMock()
        mock_dao.find.return_value = [{"email": "user@example.com", "name": "Alice"}]
        controller = UserController(dao=mock_dao)

        # Act
        result = controller.get_user_by_email("user@example.com")

        # Assert
        assert result == {"email": "user@example.com", "name": "Alice"}

    # TC4: More than 1 user found -> First user returned + warning printed
    def test_multiple_users_found(self):
        # Arrange
        mock_dao = MagicMock()
        mock_dao.find.return_value = [
            {"email": "user@example.com", "name": "Alice"},
            {"email": "user@example.com", "name": "Bob"}
        ]
        controller = UserController(dao=mock_dao)

        # Act
        result = controller.get_user_by_email("user@example.com")

        # Assert
        assert result == {"email": "user@example.com", "name": "Alice"}

    # TC5: Database operation fails -> Exception raised
    def test_database_operation_fails(self):
        # Arrange
        mock_dao = MagicMock()
        mock_dao.find.side_effect = Exception("Database error")
        controller = UserController(dao=mock_dao)

        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            controller.get_user_by_email("user@example.com")
        assert str(excinfo.value) == "Database error"