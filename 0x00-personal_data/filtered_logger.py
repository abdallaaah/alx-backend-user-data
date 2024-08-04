#!/usr/bin/env python3
""" 0. Regex-ing """
import os
import re
from typing import List
import logging
import mysql.connector
from mysql.connector import Error, MySQLConnection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """get logger function"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    data_base_name = os.getenv('PERSONAL_DATA_DB_NAME')
    try:
        connection = mysql.connector.connect(host=host, database=data_base_name, username=username, password=password)
        if connection.is_connected():
            return connection
    except Error as e:
        print('Error while connecting database', e)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """that returns the log message obfuscated: """
    for field in fields:
        message = re.sub(
            rf'{re.escape(field)}=.*?(?={separator}|$)',
            f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """format logger"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
