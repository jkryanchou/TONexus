# -*- coding=utf-8 -*-

# import csv

# from tests.factories.ton import MessageFactory
from tests.fixtures.base import BaseFixtures


class MessageFixtures(BaseFixtures):
    pass

    # @classmethod
    # def setup_top_100_messages(cls):
    #     with open('./tests/data/top_100_messages.csv', 'r') as f:
    #         reader = csv.DictReader(f, delimiter=',')
    #         for r in reader:
    #             r['ihr_disabled'] = bool(r['ihr_disabled'])
    #             r['bounce'] = bool(r['bounce'])
    #             r['bounced'] = bool(r['bounced'])
    #             r['has_init_state'] = bool(r['has_init_state'])
    #             for k, v in r.items():
    #                 if v == '\\N':
    #                     r[k] = None
    #             MessageFactory.create(**r)
