#!/usr/bin/env python3
""" module to mainpulate with logging library """
import re
import logging
from typing import List
from mysql.connector import connect
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
user = os.environ.get('PERSONAL_DATA_DB_USERNAME') or 'root'
password = os.environ.get('PERSONAL_DATA_DB_PASSWORD') or ''
host = os.environ.get('PERSONAL_DATA_DB_HOST') or 'localhost'
db = os.environ.get('PERSONAL_DATA_DB_NAME')


def get_db() -> connect:
    """ function that connect to mysql database """
    return connect(user=user, password=password, host=host, database=db)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ function that obfuscated the log message
        Params:
            - fields: a list of strings representing
                all fields to obfuscate
            - redaction: a string representing by what
                the field will be obfuscated
            - message: string representing the log line
            - separator: string representing by which character
                is separating all fields in the log line
        Return:
            log message obfuscated
    """
    for f in fields:
        pattern = re.compile(
            fr'(?<={re.escape(f)}=)(.*?)(?={re.escape(separator)})')
        message = re.sub(pattern, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ magic method start at each instance """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ method to filter values in incoming log records """
        filtered_msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        record.msg = filtered_msg
        return logging.Formatter(self.FORMAT).format(record)


def get_logger() -> logging.Logger:
    """ creating logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(log_handler)
    return logger
