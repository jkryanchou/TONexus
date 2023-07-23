# -*- coding: utf-8 -*-

import json
import traceback

from flask import Response
from flask_log_request_id import current_request_id
from werkzeug.exceptions import HTTPException

from tonexus.loggers import logger


class ConsoleRequestError(HTTPException):
    def __init__(
        self, status_code=422, error_code="PermissionDenied", message="User was not allowed to operate", request_id=""
    ):
        if not message:
            message = "request invalid, validate usage and try again"

        self.code = status_code
        self.message = message
        self.error_code = error_code
        self.request_id = request_id
        super(ConsoleRequestError, self).__init__(description=message)


def register_error_handler(app):

    @app.errorhandler(404)
    @app.errorhandler(405)
    def error_handler(e):
        return Response(
            json.dumps({"Code": Codes.NotFound, "Message": Messages.NotFound, "RequestId": current_request_id()}),
            status=404,
            mimetype="application/json",
        )

    @app.errorhandler(Exception)
    def error_handler(e):
        if isinstance(e, ConsoleRequestError):
            return Response(
                json.dumps({"Code": e.error_code, "Message": e.message, "RequestId": current_request_id()}),
                status=e.code,
                mimetype="application/json",
            )
        else:
            logger.error(traceback.format_exc())
            return Response(
                json.dumps(
                    {"Code": Codes.InternalError, "Message": Messages.InternalError, "RequestId": current_request_id()}
                ),
                status=500,
                mimetype="application/json",
            )


class Messages(object):
    Succeed = "Succeed"
    InternalError = "The request processing has failed due to some unknown error"
    ServiceUnavailable = "The request has failed due to a temporary failure of the server"
    InvalidParams = "Request invalid validate usage and try again"
    InvalidAction = "Specified action is not valid"
    Forbidden = "Check failed user has no permission"
    NotFound = "You specifiy resources were not found"
    Expired = "Your token has expired. Please login again"
    MethodNotAllowed = "Method not allowed"
    UnknowError = "Server unknown error"


class Codes(object):
    Succeed = "Succeed"  # 成功
    InternalError = "InternalError"  # 内部错误
    ServiceUnavailable = "ServiceUnavailable"  # 服务不存在
    InvalidParams = "InvalidParams"  # 参数异常
    InvalidAction = "InvalidAction"  # 操作异常
    Forbidden = "Forbidden"  # 未授权，禁止访问
    NotFound = "NotFound"  # 资源不存在
    Expired = "Expired"  # 已过期
    MethodNotAllowed = "MethodNotAllowed"  # Method 不允许
    UnknowError = "ServerError"  # 服务器故障
