#!/usr/bin/env python3
"""session class inherit from the auth"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User

class SessionAuth(Auth):
    """Basic auth inherit from Auth"""
    pass