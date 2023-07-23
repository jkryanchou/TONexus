
# -*- coding=utf-8 -*-

from flask import jsonify
from flask_log_request_id import current_request_id

from tonexus.exceptions import Codes, Messages, ConsoleRequestError


def write_json(data=None, code=Codes.Succeed, message=Messages.Succeed):
    return jsonify(Code=code, Message=message, RequestId=current_request_id(), Data=data)


def raise_not_found(msg=Messages.NotFound):
    raise ConsoleRequestError(404, Codes.NotFound, msg, request_id=current_request_id())
