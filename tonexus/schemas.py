# -*- coding=utf-8 -*-

from webargs import fields
from marshmallow import Schema, validate


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

