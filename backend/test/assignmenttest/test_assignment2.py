#Mocking is a way to replace real api with fake ones just for testing, if I have a weather api that I call, instead of using
#it in a test I just say that the weather is sunny. This way it is easier and faster to test the system, and you can test
#specific cases. It also test only the units and the functions logic and not the real api.

#We worked together in the school, requiring both of our inputs to solve this.

import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

#This test verifies that if you use an invalid user email, it raises a ValueError.
def test_email_format_invalid():
    dao = Mock()
 
    ctrl = UserController(dao)

    with pytest.raises(ValueError):
        ctrl.get_user_by_email("not-an-email")

#This test verifies that if you use an email that doesn't exist, it returns None.
def test_no_user_found():
    dao = Mock()
    dao.find.return_value = []
    ctrl = UserController(dao)

    assert ctrl.get_user_by_email("a@b.com") is None

#This is a normal verification test, testing that if you enter your email correctly.
def test_single_user_returned():
    dao = Mock()
    expected = {"id": 1, "email": "a@b.com"}
    dao.find.return_value = [expected]
    ctrl = UserController(dao)

    result = ctrl.get_user_by_email("a@b.com")
    assert result == expected

#This is testing if there are multiple users with the same email in the database both a warning is raised and the first
# user is returned
def test_multiple_users(capsys):
    dao = Mock()
    user1 = {"id": 1, "email": "a@b.com"}
    user2 = {"id": 2, "email": "a@b.com"}
    dao.find.return_value = [user1, user2]
    ctrl = UserController(dao)

    result = ctrl.get_user_by_email("a@b.com")
    captured = capsys.readouterr()
    assert ("more than one user found with mail a@b.com" in captured.out and result == user1)

#This is testing if the database throws an exception
def test_dao_exception():
    dao = Mock()
    dao.find.side_effect = Exception("Database error")
    ctrl = UserController(dao)

    with pytest.raises(Exception):
        ctrl.get_user_by_email("a@b.com")
