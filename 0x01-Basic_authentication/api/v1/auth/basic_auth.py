#!/usr/bin/env python3
""" module that handle basicauth class """
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ class inherit from auth class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ check if header is valid base64 or not
        """
        if authorization_header and type(authorization_header) is str:
            auth_head_split = authorization_header.split(' ')
            if auth_head_split[0] == 'Basic':
                return auth_head_split[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ method that return decode64 of string
        """
        base = base64_authorization_header
        if base and type(base) is str:
            try:
                string = base64.b64decode(base).decode('ascii')
                return string
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ method extract user email and password from string
        """
        string = decoded_base64_authorization_header
        if string and type(string) is str:
            if ':' in string:
                return tuple(string.split(':'))
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ methods get user object based on provided creditals
        """
        if type(user_email) is str and type(user_pwd) is str:
            users = User.search({'email': user_email})
            if len(users) > 0:
                user = users[0]
                if (user.is_valid_password(user_pwd)):
                    return user
        return None
