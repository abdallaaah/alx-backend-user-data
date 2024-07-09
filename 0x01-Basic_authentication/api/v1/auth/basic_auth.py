#!/usr/bin/env python3
"""Basic class inherit from the auth"""
from .auth import Auth
import base64


class BasicAuth(Auth):
    """Basic auth inherit from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """return none in some casses or base64"""
        if authorization_header is None or type(authorization_header) != str:
            return None
        if authorization_header and type(authorization_header) == str:
            list = authorization_header.split(' ')
            if list[0] != 'Basic':
                return None
            else:
                return list[1]
