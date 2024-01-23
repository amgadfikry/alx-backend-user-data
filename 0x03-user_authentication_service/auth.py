#!/usr/bin/env python3
""" module for authorization """
import bcrypt
from db import DB
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ create new uuid string
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ magic init instance method
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ method check if email in register before
        """
        try:
            self._db.find_user_by(email=email)
        except Exception:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ check if valid user and password
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
        except Exception:
            return False
