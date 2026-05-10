from src.controllers.controller import Controller
from src.util.dao import DAO

import re

# Stricter regex: requires local-part, @, domain, dot, and host
emailValidator = re.compile(r'^[^@]+@[^@]+\.[^@]+$')

class UserController(Controller):
    def __init__(self, dao: DAO):
        super().__init__(dao=dao)

    def get_user_by_email(self, email: str):

        # Fix 1: Guard against None and non-string input before regex check
        if not isinstance(email, str) or not re.fullmatch(emailValidator, email):
            raise ValueError('Error: invalid email address')

        try:
            users = self.dao.find({'email': email})

            # Fix 2: Handle the zero-result case — return None instead of crashing
            if len(users) == 0:
                return None
            elif len(users) == 1:
                return users[0]
            else:
                # Fix 3: Warning still printed, but now guarded by proper length check
                print(f'Error: more than one user found with mail {email}')
                return users[0]

        except Exception as e:
            raise

    def update(self, id, data):
        try:
            update_result = super().update(id=id, data={'$set': data})
            return update_result
        except Exception as e:
            raise