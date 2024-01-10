#!/usr/bin/env python3
""" check password encryption """
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that expects one string argument name password
        and returns a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check if password same as hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
