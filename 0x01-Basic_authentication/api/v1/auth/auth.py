#!/usr/bin/env python3
""" module that handle auth class """
from flask import request
from typing import TypeVar, List


class Auth:
    """ class of auth that contain all auth methods
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ method determine with path in excluded path or not
            Return:
                True: if not in excluded path
                False if path in excluded path
        """
        if path and (excluded_paths and len(excluded_paths) > 0):
            if path[len(path) - 1] != '/':
                path = path[:] + '/'
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ method which create auth header
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user
        """
        return request