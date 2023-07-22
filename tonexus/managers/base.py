# -*- coding=utf-8 -*-

import logging


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(object, metaclass=SingletonMeta):

    name = "mananger"

    def __init__(self, name="", log_level=logging.INFO):
        name = name if name else self.name