#!/usr/bin/env python3
"""Basic class inherit from the auth"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User

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

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """check if user creadintails is on database and return user if yes"""
        if not user_email or not user_pwd:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        x = {'email': user_email}
        users = User.search(x)
        if users:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
                else:
                    return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)

        if not auth_header:
            return None

        encoded = self.extract_base64_authorization_header(auth_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)

        if not email or not pwd:
            return None

        user = self.user_object_from_credentials(email, pwd)

        return user
