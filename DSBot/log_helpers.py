""" Module to setup the logger.

How to use the logger:
    logger = logging.getLogger(__name__)
    logger.info("A message with a %s", "parameter")

Levels explanation:
- DEBUG: for code related stuff (entering a function...)
- INFO: for standard logging (user logged in...)
- WARNING: if something is wrong (wrong configuration...)
- ERROR: if what went wrong was unexpected (strange requests from client...)
- CRITICAL: if the situation is not recoverable
"""
import logging
import os

import click


class RemoveColorFilter(logging.Filter):
    """ Remove ANSI colors.

    Adapted from https://stackoverflow.com/questions/64239799/
    """

    def filter(self, record):
        if record and record.name == 'werkzeug':
            record.msg = click.unstyle(record.msg)
        return True


def setup_logger(prefix: str = ''):
    """ This function sets up the logging module.

    If provided, the prefix is applied to the log files name.
    If env LOG_TO_FILE is defined, then the logger will also output to file.
    """
    # Set root logger to accept all messages
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    logging.getLogger("matplotlib.font_manager").setLevel(logging.INFO)

    # Log string: prefix 2003-07-08 16:49:45,896 Logger.Name LEVEL Message
    format_s = f"%(asctime)s %(name)s %(levelname)s %(message)s"
    formatter = logging.Formatter(format_s)

    if "LOG_TO_FILE" in os.environ:
        # Save all the log messages to file
        file_h = logging.FileHandler(f"{prefix}complete.log")
        file_h.setLevel(logging.DEBUG)
        file_h.setFormatter(formatter)
        file_h.addFilter(RemoveColorFilter())
        root.addHandler(file_h)

        # Keep a file with error messages
        error_h = logging.FileHandler(f"{prefix}errors.log")
        error_h.setLevel(logging.ERROR)
        error_h.setFormatter(formatter)
        file_h.addFilter(RemoveColorFilter())
        root.addHandler(error_h)

    # Print all messages to console
    stream_h = logging.StreamHandler()
    stream_h.setLevel(logging.DEBUG)
    stream_h.setFormatter(formatter)
    stream_h.addFilter(RemoveColorFilter())
    root.addHandler(stream_h)

    logging.getLogger(__name__).debug("completed logging setup")
