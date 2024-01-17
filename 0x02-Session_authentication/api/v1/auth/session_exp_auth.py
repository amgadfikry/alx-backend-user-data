#!/usr/bin/env python3
""" module that handle session expire auth class """
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ class for session has expire date
    """
    def __init__(self):
        """ magic method start in every instance
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """ method for creation of session with duration
        """
        session_id = super().create_session(user_id)
        if session_id:
            session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_dict
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ method for get user id based on session id
        """
        session_dict = super().user_id_for_session_id(session_id)
        if session_dict:
            if self.session_duration <= 0:
                return session_dict['user_id']
            s_created = session_dict.get('created_at')
            if s_created:
                time_sec = timedelta(seconds=self.session_duration)
                if s_created + time_sec > datetime.now():
                    return session_dict['user_id']
        return None
