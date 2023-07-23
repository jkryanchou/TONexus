# -*- coding=utf-8 -*-

from flask_testing import TestCase
from sqlalchemy.sql import text  # REF: https://stackoverflow.com/questions/54483184/sqlalchemy-warning-textual-column-expression-should-be-explicitly-declared

# from tonexus.ext import db
from tonexus.app import create_app


class BaseManagerTestCase(TestCase):

    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        pass
        # db.create_all()

    def tearDown(self):
        pass
        # # REF: https://gist.github.com/vkotovv/6281951
        # meta = self.app.db.metadata
        # for table in reversed(meta.sorted_tables):
        #     # self._app.db.session.execute(table.delete())  # Truncate table
        #     # NOTE: This is for PostgreSQL
        #     self.app.db.session.execute(
        #         text("TRUNCATE TABLE {} CASCADE;".format(table.fullname))
        #     )
        #     self.app.db.session.commit()
        #     # self._logger.info("<{}> truncated.".format(table.fullname))
