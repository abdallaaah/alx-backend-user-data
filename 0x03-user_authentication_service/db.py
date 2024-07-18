#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.inspection import inspect


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """add user to users table"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find user by it is email"""
        session = self.__session
        columns = [column.name for column in inspect(User).c]
        for key in kwargs:
            if key not in columns:
                raise InvalidRequestError()
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except (NoResultFound and InvalidRequestError) as e:
            raise e

    def update_user(self, id, **kwargs) -> None:
        """update user"""
        session = self.__session
        for key, item in kwargs.items():
            keyy = key
            password = item
        columns = [column.name for column in inspect(User).c]
        if keyy not in columns or not isinstance(id, int):
            raise ValueError
        user = self.find_user_by(id=id)
        user.hashed_password = password
        session.commit()
        return None
