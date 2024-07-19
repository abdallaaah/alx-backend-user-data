#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.inspection import inspect
from typing import Any, Dict
from user import Base, User
from sqlalchemy.orm.session import Session
class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user to users table"""
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        # self._Session.remove()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """Find a user by specified attributes.

        Raises:
            NoResultFound: When no results are found.
            InvalidRequestError: When invalid query arguments are passed

        Returns:
            User: First row found in the `users` table.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, id: int, **kwargs: Dict[str, Any]) -> None:
        """Update user"""
        session = self._session
        user = self.find_user_by(id=id)
        if user:
            if kwargs:
                columns = [column.name for column in inspect(User).c]
                for key, value in kwargs.items():
                    if key not in columns:
                        raise ValueError(f"Invalid column name: {key}")
                    if key == 'session_id':
                        user.session_id = value
                    setattr(user, key, value)
                session.commit()
        return None
