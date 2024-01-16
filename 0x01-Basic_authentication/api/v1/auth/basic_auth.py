#!/usr/bin/env python3
""" module that handle basicauth class """
from api.v1.auth.auth import Auth
import base64


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
        if base64_authorization_header\
        and type(base64_authorization_header) is str:
            try:
                string = base64.b64decode(
                    base64_authorization_header).decode('ascii')
                return string
            except Exception:
                return None
        return None
