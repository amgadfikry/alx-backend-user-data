#!/usr/bin/env python3
""" module that handle auth class """
from flask import request


class Auth:
    """ class of auth that contain all auth methods
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ method determine with path need auth
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ method which create auth header
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user
        """
        return request
