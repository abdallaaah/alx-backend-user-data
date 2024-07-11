#!/usr/bin/env python3
"""Basic class inherit from the auth"""
from .auth import Auth
import base64
import binascii


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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """return decoded value of the auth string"""
        if (not base64_authorization_header
                or not isinstance(base64_authorization_header, str)):
            return None

        try:
            x = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        return x.decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """extract mail and password or return none if not : in the auth"""
        if not decoded_base64_authorization_header or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        name, password = decoded_base64_authorization_header.split(':')
        return (name, password)
