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
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password


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
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        user = self._db.find_user_by(email=email)
        if user:
            password = password.encode('utf-8')
            if bcrypt.checkpw(password, user.hashed_password):
                return True
            else:
                return False

    def create_session(self, email: str) -> str or None:
        """create session is mail is valid"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> user.User or None:
        """grt user from session_id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if not user:
                return None
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroy session and update session id to none"""
        try:
            user_id = int(user_id)
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db.update_user(user_id, session_id=None)
        except (NoResultFound, InvalidRequestError):
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """generate session_id"""
        try:
            user = self._db.find_user_by(email=email)
            if user is None or email is None:
                raise ValueError()
            reset_token = uuid.uuid4()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        except InvalidRequestError:
            raise ValueError()
        except InvalidRequestError:
            raise ValueError()
