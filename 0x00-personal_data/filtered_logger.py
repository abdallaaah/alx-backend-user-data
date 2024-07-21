#!/usr/bin/env python3
""" 0. Regex-ing """
import logging
import re

logger = logging.getLogger(__name__)


def filter_datum(fields, redaction, message, separator):
    """that returns the log message obfuscated: """
    for field in fields:
        message = re.sub(
            rf'{re.escape(field)}=.*?(?={separator}|$)',
            f'{field}={redaction}', message)
    return message
