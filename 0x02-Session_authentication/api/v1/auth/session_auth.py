#!/usr/bin/env python3
""" module that handle session auth class """
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ class inherit from Auth and represent session auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ method that generate session id based on user id
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None
