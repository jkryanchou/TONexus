# -*- coding=utf-8 -*-

import os

from dotenv import load_dotenv


class Config(object):
    """
    Tonexus 统一配置
    """

    load_dotenv()

    TZ_DELTA_HOUR = 8  # 时区差值

    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

    # App Startup
    APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.environ.get("APP_PORT", "8080"))

    # Database
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT_STRING = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "ton_index")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASS = os.environ.get("DB_PASS", "postgrespass")
    DB_CHARSET = os.environ.get("DB_CHARSET", "utf8mb4")

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{db_password}@{host}:{port}/{dbname}'.format(
        host=DB_HOST, port=DB_PORT_STRING, user=DB_USER, db_password=DB_PASS, dbname=DB_NAME
    )
    
    # TON RPC Endpoint
    TON_RPC_ENDPOINT = os.environ.get("TON_RPC_ENDPOINT", "http://35.230.25.197:8081")
    TON_GET_ADDR_BALANCE = f"{TON_RPC_ENDPOINT}/getAddressBalance"

    # Log 系统日志相关
    LOG_ROTATE_PATH = os.environ.get("LOG_ROTATE_PATH", "./tonexus.logs")
    LOG_ROTATE_SIZE = 50 * 1024 * 1024  # 50MB
    LOG_ROTATE_COUNT = 5
    LOG_LEVEL = os.environ.get("LOG_LEVEL", 'INFO')  # Force uppercase
