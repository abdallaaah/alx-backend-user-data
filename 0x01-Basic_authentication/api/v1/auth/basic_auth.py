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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Return Decode of auth user"""
        if (base64_authorization_header is None or
                type(base64_authorization_header) != str):
            return None
        try:
            decodes_bytes = base64.b64decode(base64_authorization_header)
            return decodes_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None
