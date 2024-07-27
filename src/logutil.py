"""
Custom logging script

Code taken from my contributions in:
https://github.com/savioxavier/repo-finder-bot/
Additional thanks to savioxavier
"""

import logging
from config import DEBUG  # pylint: disable=import-error # This works fine?


class CustomFormatter(logging.Formatter):
    """Custom formatter class"""

    grey = "\x1b[38;1m"
    green = "\x1b[42;1m"
    yellow = "\x1b[43;1m"
    red = "\x1b[41;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # format = "[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s"
    FORMATS = (
        {
            logging.DEBUG: green
            + f"{reset}[%(asctime)s]{green}[%(levelname)-7s][%(name)-14s]\
{reset}[{red}%(lineno)4s{reset}] %(message)s"
            + reset,
            logging.INFO: grey
            + f"{reset}[%(asctime)s]{grey}[%(levelname)-7s][%(name)-14s]\
{reset}[{red}%(lineno)4s{reset}] %(message)s"
            + reset,
            logging.WARNING: yellow
            + f"[%(asctime)s][%(levelname)-7s][%(name)-14s]\
[{red}%(lineno)4s{reset}{yellow}] %(message)s"
            + reset,
            logging.ERROR: red
            + "[%(asctime)s][%(levelname)-7s][%(name)-14s]\
[%(lineno)4s] %(message)s"
            + reset,
            logging.CRITICAL: bold_red
            + "[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s"
            + reset,
        }
        if DEBUG
        else {
            logging.DEBUG: reset,
            logging.INFO: grey + "[%(asctime)s][%(levelname)7s] %(message)s" + reset,
            logging.WARNING: yellow
            + "[%(asctime)s][%(levelname)7s] %(message)s"
            + reset,
            logging.ERROR: red + "[%(asctime)s][%(levelname)7s] %(message)s" + reset,
            logging.CRITICAL: bold_red
            + "[%(asctime)s][%(levelname)7s] %(message)s"
            + reset,
        }
    )

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%I:%M.%S%p")
        return formatter.format(record)


def overwrite_ipy_loggers():
    for k, v in logging.Logger.manager.loggerDict.items():
        print(k, v)
        if k in ["mixin", "dispatch", "http", "gateway", "client", "context"]:
            for h in v.handlers:
                h.setFormatter(CustomFormatter)


def get_logger(name):
    """Function to get a logger
    Useful for modules that have already initialized a logger, such as discord.py
    """
    __logger = logging.getLogger(name)
    __logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    __ch = logging.StreamHandler()
    __ch.setFormatter(CustomFormatter())
    __logger.addHandler(__ch)
    return __logger


def init_logger(name="root"):
    """Function to create a designated logger for separate modules"""
    __logger = logging.Logger(name)
    __ch = logging.StreamHandler()
    __ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    __ch.setFormatter(CustomFormatter())
    __logger.addHandler(__ch)
    return __logger
