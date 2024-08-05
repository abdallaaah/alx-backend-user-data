#!/usr/bin/env python3
""" 0. Regex-ing """
import os
import re
from typing import List
import logging
import mysql.connector
from mysql.connector import Error, MySQLConnection

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    string = []
    logger = get_logger()
    field_names = [i[0] for i in cursor.description]
    for row in cursor:
        row_dict = dict(zip(field_names, row))
        user_list = []
        for key, value in row_dict.items():
            if (key == 'name' or key == 'email' or
                    key == 'phone' or key == 'ssn'
                    or key == 'password'):
                value = '***'
            user_list.append(f"{key}={value}")
        sepaerator = '; '
        x = sepaerator.join(user_list)
        logger.log(logging.INFO, x)
    cursor.close()
    db.close()


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
    """check db conntection and return connection"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    data_base_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(host=host,
                                         database=data_base_name,
                                         user=username,
                                         password=password)
    return connection


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


if __name__ == '__main__':
    main()
