"""
Unit tests for get_user_by_email function
PA1417 Assignment 2
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the backend directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controllers.usercontroller import UserController, DAO

# Mock data that simulates database records
MOCK_USERS = {
    "test@edutask.com": {
        "email": "test@edutask.com",
        "name": "Test User",
        "user_id": "12345"
    },
    "john@example.com": {
        "email": "john@example.com", 
        "name": "John Doe",
        "user_id": "67890"
    }
}

class TestGetUserByEmail:
    
    def setup_method(self):
        """Create a UserController with a mocked DAO before each test"""
        self.mock_dao = Mock(spec=DAO)
        self.controller = UserController(dao=self.mock_dao)
    
    def test_tc1_valid_existing_email(self):
        """TC1: Valid email that exists should return user"""
        self.mock_dao.find.return_value = [MOCK_USERS["test@edutask.com"]]
        result = self.controller.get_user_by_email("test@edutask.com")
        assert result is not None
        assert result["email"] == "test@edutask.com"
        self.mock_dao.find.assert_called_with({'email': 'test@edutask.com'})
    
    def test_tc2_non_existent_email(self):
        """TC2: Valid email format but not in database should return None"""
        self.mock_dao.find.return_value = []
        result = self.controller.get_user_by_email("fake@nowhere.com")
        assert result is None
    
    def test_tc3_empty_string_raises_error(self):
        """TC3: Empty string should raise ValueError"""
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("")
    
    def test_tc4_none_value_raises_error(self):
        """TC4: None should raise ValueError (currently raises TypeError - bug)"""
        with pytest.raises(ValueError):
            self.controller.get_user_by_email(None)
    
    def test_tc5_invalid_format_no_at_raises_error(self):
        """TC5: Missing @ symbol should raise ValueError"""
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("notanemail")
    
    def test_tc6_invalid_format_missing_domain_raises_error(self):
        """TC6: Missing domain part should raise ValueError"""
        # Bug: regex '.*@.*' accepts "user@" - validation is too permissive
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("user@")
    
    def test_tc7_multiple_users_with_same_email(self):
        """TC7: Multiple users with same email - should return first and print warning"""
        multiple_users = [
            {"email": "duplicate@test.com", "name": "User1", "user_id": "001"},
            {"email": "duplicate@test.com", "name": "User2", "user_id": "002"}
        ]
        self.mock_dao.find.return_value = multiple_users
        
        result = self.controller.get_user_by_email("duplicate@test.com")
        
        # SINGLE DEFINITIVE ASSERT: Verify it extracts the primary dictionary payload matching first record
        assert result == {"email": "duplicate@test.com", "name": "User1", "user_id": "001"}
    
    def test_tc8_whitespace_email(self):
        """TC8: Email with spaces should be rejected"""
        # Bug: regex accepts whitespace - validation should strip or reject
        with pytest.raises(ValueError, match="invalid email address"):
            self.controller.get_user_by_email("  test@edutask.com  ")
    
    def test_tc9_database_exception(self):
        """TC9: Database error should propagate the exception"""
        self.mock_dao.find.side_effect = Exception("Database connection failed")
        
        # SINGLE DEFINITIVE ASSERT: Verify that the exact database exception surfaces unmodified
        with pytest.raises(Exception, match="Database connection failed"):
            self.controller.get_user_by_email("test@edutask.com")