# -*- coding: utf-8 -*-

import re
import logging

from webargs.flaskparser import FlaskParser
from tonexus.config import Config
from tonexus.exceptions import ConsoleRequestError


class MyFlaskParser(FlaskParser):

    def handle_error(self, error, req, schema, error_status_code, error_headers):
        status_code = getattr(error, "status_code", self.DEFAULT_VALIDATION_STATUS)

        if status_code == 422:
            error.code = "InvalidParams"
            if Config.DEBUG:
                error.messages = str(error)
            else:
                error.messages = "request invalid, validate usage and try again"
                logging.warning(str(error))

        raise ConsoleRequestError(422, error.code, str(error.messages))

    def convert_to_snake_case(self, kw):
        # REF: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        result = {}
        for k, v in kw.items():
            ck = re.sub(r"(?<!^)(?=[A-Z])", "_", k).lower()
            if isinstance(v, dict):
                result[ck] = self.convert_to_snake_case(v)
            elif isinstance(v, list):
                result[ck] = [self.convert_to_snake_case(i) if isinstance(i, dict) else i for i in v]
            else:
                result[ck] = v
        return result

    @staticmethod
    def convert_to_upper_camel_case(kw):
        """下划线转大驼峰法命名,只转最外层key"""
        result = {}
        for k, v in kw.items():
            s = re.sub("_([a-zA-Z])", lambda m: (m.group(1).upper()), k)
            result[s[0].upper() + s[1:]] = v
        return result

    def convert_to_upper_camel_case_recursion(self, kw):
        """下划线转大驼峰法命名,递归所有key"""
        result = {}
        for k, v in kw.items():
            if isinstance(v, dict):
                v = self.convert_to_upper_camel_case_recursion(v)
            elif isinstance(v, list):
                v = [self.convert_to_upper_camel_case_recursion(i) for i in v]
            s = re.sub("_([a-zA-Z])", lambda m: (m.group(1).upper()), k)
            result[s[0].upper() + s[1:]] = v
        return result


parser = MyFlaskParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
