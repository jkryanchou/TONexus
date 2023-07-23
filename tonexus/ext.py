# -*- coding=utf-8 -*-

from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from tonexus.config import Config


db = SQLAlchemy()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_size=20, pool_recycle=1800)
