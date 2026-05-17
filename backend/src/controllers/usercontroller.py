from src.controllers.controller import Controller
from src.util.dao import DAO

import re

emailValidator = re.compile(r'.*@.*')

class UserController:

    def __init__(self, dao):
        self.dao = dao

    def get_user_by_email(self, email: str):
        """Given a valid email address of an existing account, return the user object contained in the database associated
        to that user. For now, do not assume that the email attribute is unique. Additionally print a warning message containing the email
        address if the search returns multiple users.

        parameters:
            email -- an email address string

        returns:
            user -- the user object associated to that email address (if multiple users are associated to that email: return the first one)
            None -- if no user is associated to that email address

        raises:
            ValueError -- in case the email parameter is not valid (i.e., conforming <local-part>@<domain>.<host>)
            Exception -- in case any database operation fails
        """

        # FIX 1: Check None before regex to prevent TypeError
        if email is None:
            raise ValueError('Error: invalid email address')

        # FIX 2: Stricter regex — requires at least one character before AND after @
        strictValidator = re.compile(r'.+@.+')
        if not re.fullmatch(strictValidator, email):
            raise ValueError('Error: invalid email address')

        try:
            users = self.dao.find({'email': email})

            # FIX 3: Handle empty list — return None instead of IndexError
            if len(users) == 0:
                return None

            if len(users) == 1:
                return users[0]
            else:
                print(f'Error: more than one user found with mail {email}')
                return users[0]

        except Exception as e:
            raise Exception(f'Error: database operation failed: {e}')