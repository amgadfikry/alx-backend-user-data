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

    def create_session(self, email: str):
        """ create session id and add it to database
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(
                    user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str):
        """ get user by session id
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except Exception:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """ destory session_id and make it none
        """
        user = self._db.find_user_by(id=user_id)
        self._db.update_user(
                user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ method that generate reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(
                    user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update password and reset token to none
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                    user.id, hashed_password=_hash_password(password),
                    reset_token=None)
            return None
        except Exception:
            raise ValueError
