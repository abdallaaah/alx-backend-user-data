#!/usr/bin/env python3
""""auth function """
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt


def _hash_password(password: str) -> bytes:
    """return hasehd password from the saulted password
    utf-8 password -> salted (random text added to password)
    -> hash the salt
    """
    if password:
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> any:
        """regestir user function """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {user.email} already exists')

        except NoResultFound:
            hash = _hash_password(password)
            user = self._db.add_user(email, hash)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """check is valid login or not"""
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode('utf-8')
            if bcrypt.checkpw(password, user.hashed_password):
                return True
            else:
                return False
        except NoResultFound and InvalidRequestError:
            return False
