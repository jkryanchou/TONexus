# -*- coding=utf-8 -*-

import random
import time

from tonexus.app import create_app
from tonexus.loggers import logger


class BaseFixtures(object):

    def __init__(self, app=create_app(), name="asset"):
        random.seed(time.time())
        self._app = app
        self._logger = logger

    def setup(self):
        raise NotImplemented

    @classmethod
    def from_app(cls, app):
        return cls(app)
