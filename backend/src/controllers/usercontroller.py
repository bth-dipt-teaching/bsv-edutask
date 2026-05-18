from src.controllers.controller import Controller
from src.util.dao import DAO

import re
emailValidator = re.compile(r'.*@.*')

class UserController(Controller):
    def __init__(self, dao: DAO):
        super().__init__(dao=dao)

    def get_user_by_email(self, email: str):

        if not emailValidator.fullmatch(email):
            raise ValueError('Error: invalid email address')

        try:
            users = self.dao.find({'email': email})

            if len(users) == 0:
                return None

            if len(users) > 1:
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