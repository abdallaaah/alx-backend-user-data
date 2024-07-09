#!/usr/bin/env python3
"""auth basics class"""
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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """check current user"""
        return None
