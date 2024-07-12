#!/usr/bin/env python3
"""auth basics class"""
import os

from flask import request
from typing import List, TypeVar


class Auth():
    """the Basic auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """if path not excluded so it is need auth"""
        if path is not None:
            if path[-1] != '/':
                path += '/'
        if (path is None or excluded_paths is None or
                excluded_paths == [] or path not in excluded_paths):
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """request is Flask object"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """check current user"""
        return None

    def session_cookie(self, request=None):
        """return cookie which hold the session_id"""
        if not request:
            return None
        session_name_env = os.getenv('SESSION_NAME')
        session_id = request.cookies.get(f'{session_name_env}')
        return session_id
