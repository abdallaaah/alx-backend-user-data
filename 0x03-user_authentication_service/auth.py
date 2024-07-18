#!/usr/bin/env python3
""""auth function """
import uuid

import user
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


def _generate_uuid() -> str:
    """generate random uuid.4 for user session_id """
    id = str(uuid.uuid4())
    return id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str)\
            -> user.User or ValueError:
        """regestir user function """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')

        except NoResultFound:
            hash = _hash_password(password)
            user = self._db.add_user(email, hash)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login is valid."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                # Compare the provided password with the stored hashed password
                if bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password):
                    return True
                else:
                    return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str or None:
        """create session is mail is valid"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db.update_user(id=user.id, session_id=session_id)
            return session_id
        except NoResultFound and InvalidRequestError:
            return None
