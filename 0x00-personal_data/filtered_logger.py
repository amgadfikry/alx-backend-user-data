#!/usr/bin/env python3
""" module to mainpulate with logging library """
import re
import logging
from typing import List


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
