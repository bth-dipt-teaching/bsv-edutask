from src.controllers.controller import Controller
from src.util.dao import DAO

import re
emailValidator = re.compile(r'.*@.*')

class UserController(Controller):
    def __init__(self, dao: DAO):
        super().__init__(dao=dao)

    def get_user_by_email(self, email: str):
        # Venu: Refined regex to ensure standard <local-part>@<domain>.<host> format
        # as required by the project specification
        if not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Error: invalid email address format')

        try:
            users = self.dao.find({'email': email})
            if len(users) == 0:
                return None
            if len(users) > 1:
                # Venu: Added clearer warning for non-unique email attributes
                print(f'Warning: Multiple users ({len(users)}) found for email: {email}')
            return users[0]
        except Exception as e:
            print(f"Database operation failed: {e}")
            raise

    def update(self, id, data):
        try:
            update_result = super().update(id=id, data={'$set': data})
            return update_result
        except Exception as e:
            raise