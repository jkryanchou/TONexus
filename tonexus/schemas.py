# -*- coding=utf-8 -*-

import inspect

from webargs import fields
from marshmallow import Schema, validate

class Constant(object):
    @classmethod
    def values(cls):
        # REF: https://stackoverflow.com/questions/9058305/getting-attributes-of-a-class
        attrs = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [a[1] for a in attrs if not (a[0].startswith("__") and a[0].endswith("__"))]

    @classmethod
    def items(cls):
        attrs = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return dict(a for a in attrs if not (a[0].startswith("__") and a[0].endswith("__")))

    @classmethod
    def keys(cls):
        # REF: https://stackoverflow.com/questions/9058305/getting-attributes-of-a-class
        attrs = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [a[0] for a in attrs if not (a[0].startswith("__") and a[0].endswith("__"))]


# TODO: validate parameters

class Limit(object):

    PageSize = validate.Range(min=5, max=100)
    PageNum = validate.Range(min=1)


class ListGroupedTransactionsByAddressSchema(Schema):

    Address = fields.Str(required=True)
    Direction = fields.Str(validate=validate.OneOf(["Send", "Receive"]))
    PageNum = fields.Int(load_default=1, validate=Limit.PageNum)
    PageSize = fields.Int(load_default=100, validate=Limit.PageSize)


class ListGroupedTransactionsByTXHashSchema(Schema):

    Hash = fields.Str(required=True)


class ListGroupedTransactionsByMsgHashSchema(Schema):

    Hash = fields.Str(required=True)


class ListTransactionsBetweenAddresses(Schema):

    Source = fields.Str(required=True)
    Destination = fields.Str(required=True)


class GetAddressStats(Schema):

    Address = fields.Str(required=True)

