#!/usr/bin/env python3
""" module for session db """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ class to save session to db """
    def create_session(self, user_id=None):
        """ creates and stores new instance of UserSession
        """
        session_id = super().create_session(user_id)
        if session_id:
            dic = {'user_id': user_id, 'session_id': session_id}
            user_s = UserSession(**dic)
            user_s.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """ returns the User ID by requesting UserSession
            in the database based on session_id
        """
        try:
            user_s = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(user_s) > 0:
            time_sec = timedelta(seconds=self.session_duration)
            if user_s[0].created_at + time_sec > datetime.utcnow():
                return user_s[0].user_id
            user_s[0].remove()
        return None

    def destroy_session(self, request=None):
        """ destroy session object
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                try:
                    user_s = UserSession.search({'session_id': session_id})
                except Exception:
                    return None
                user_s[0].remove()
                return True
        return False
