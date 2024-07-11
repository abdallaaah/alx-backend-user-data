#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from models.user import User


User.load_from_file()