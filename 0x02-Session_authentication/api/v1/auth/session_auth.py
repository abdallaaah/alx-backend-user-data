#!/usr/bin/env python3
"""session class inherit from the auth"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Basic auth inherit from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session id and assign it to the dic"""
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({f"{session_id}": f"{user_id}"})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrive the value of the seession_id which is the user_id"""
        if not session_id and not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(f'{session_id}')
        return user_id
