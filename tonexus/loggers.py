# -*- coding=utf-8 -*-

import logging
import logging.handlers

from tonexus.config import Config


class Logger(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def stdout_handler():
        handler = logging.StreamHandler()
        fmt = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        return handler

    @staticmethod
    def file_handler():
        handler = logging.handlers.RotatingFileHandler(
            filename=Config.LOG_ROTATE_PATH,
            maxBytes=Config.LOG_ROTATE_SIZE,
            backupCount=Config.LOG_ROTATE_COUNT,
        )
        fmt = logging.Formatter(
            fmt='{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
        )
        handler.setFormatter(fmt)
        return handler

    @staticmethod
    def create():
        stream_logger = logging.getLogger(__name__)
        stream_logger.addHandler(Logger.stdout_handler())
        stream_logger.addHandler(Logger.file_handler())
        try:
            lv = getattr(logging, Config.LOG_LEVEL.upper())
            stream_logger.setLevel(lv)
        except AttributeError:
            raise AttributeError(
                "Invalid log level: {}".format(Config.LOG_LEVEL))
        return stream_logger


logger = Logger().create()
