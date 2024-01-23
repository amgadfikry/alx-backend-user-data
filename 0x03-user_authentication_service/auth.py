#!/usr/bin/env python3
""" module for authorization """
import bcrypt


def _hash_password(password: str) -> str:
    """ hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
