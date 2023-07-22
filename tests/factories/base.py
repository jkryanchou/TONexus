# -*- coding=utf-8 -*-

import factory
from faker import Faker

from tonexus.ext import db


faker_gen = Faker(locale="zh_CN")


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        # REF: https://factoryboy.readthedocs.io/en/stable/orms.html#factory.alchemy.SQLAlchemyOptions.sqlalchemy_session_persistence
        # commit to save to db
        sqlalchemy_session_persistence = "commit"
        # 初始化 Faker
        factory.Faker.override_default_locale("zh_CN")
