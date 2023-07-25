# -*- coding=utf-8 -*-

from flask import Flask, Blueprint
from flask_log_request_id import RequestID

from tonexus.ext import db
from tonexus import routes
from tonexus.config import Config
from tonexus.exceptions import register_error_handler


def register_blueprints(app):
    """
    注册蓝图
    :param app: flask app
    :return: None
    """

    for blueprint in vars(routes).values():
        if isinstance(blueprint, Blueprint):
            app.register_blueprint(blueprint)


def register_db(app):
    """
    注册数据库
    :param app: flask app
    :return: None
    """
    db.init_app(app)
    db.app = app
    app.db = db # ref: https://stackoverflow.com/questions/45860068/accessing-a-database-created-with-flask-sqlalchemy-from-a-separate-flask-ap


def register_request_id(app):
    RequestID(app)


def register_cors(app):

    @app.after_request
    def after_request(response):
        # Ref: https://github.com/axios/axios/issues/569 using axios in front-end should set Access-Control-Allow-Origin
        response.headers.add('Access-Control-Allow-Origin', "*")
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')
        return response


def create_app():
    """
    创建APP
    :return: flask app
    """

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI  # 数据库连接 URI
    app.config["SQLALCHEMY_ECHO"] = Config.DEBUG
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # 禁用修改追踪系统，提升性能
    app.config["JSON_AS_ASCII"] = False  # 关闭默认编码，防止中文被编码成unicode

    RequestID(app)
    register_blueprints(app)
    register_db(app)
    register_error_handler(app)
    register_request_id(app)
    register_cors(app)

    return app
