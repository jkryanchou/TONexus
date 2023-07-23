# -*- coding=utf-8 -*-

from functools import wraps

from flask import request

from tonexus.libs import parser


def require_params(cls, position="json"):
    def require_params_wrap(func):
        @wraps(func)
        def require_params_decorated(*args, **kwargs):
            args_body = parser.parse(cls(), request, location=position)
            snake_case_args = parser.convert_to_snake_case(args_body)
            return func(args=snake_case_args)

        return require_params_decorated
    return require_params_wrap
