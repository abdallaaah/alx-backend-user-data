#!/usr/bin/env python3
""""auth function """
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """return hasehd password from the saulted password
        utf-8 password -> salted (random text added to password)
        -> hash the salt
        """
        if password:
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)
            return hash

    def register_user(self, email, password):
        """regestir user function """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {user.email} already exists')

        except NoResultFound:
            hash = self._hash_password(password)
            user = self._db.add_user(email, hash)
            return user

        if not user:
            print('no useeeeer')
