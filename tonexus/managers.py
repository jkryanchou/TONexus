# -*- coding=utf-8 -*-

import logging

import httpx
from sqlalchemy import func, distinct

from tonexus.models import (
    Message as MessageModel,
    Transaction as TransactionModel,
)
from tonexus.config import Config


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(object, metaclass=SingletonMeta):

    name = "mananger"

    def __init__(self, name="", log_level=logging.INFO):
        name = name if name else self.name


class TONManager(Singleton):

    def get_transactions_between_addresses(self, sender='', receiver='', page_num=1, page_size=100):
        offset = (page_num - 1) * page_size
        msg_query = MessageModel.query.filter(MessageModel.source == sender)\
                                      .filter(MessageModel.destination == receiver)\
                                      .with_entities(
                                            MessageModel.source,
                                            MessageModel.destination,
                                            MessageModel.value,
                                            MessageModel.out_tx_id
                                      )\
                                      .subquery()\
                                      .alias('msg')

        transactions = TransactionModel.query.session.query(msg_query)\
                                             .outerjoin(TransactionModel, TransactionModel.tx_id == msg_query.c.out_tx_id)\
                                             .with_entities(
                                                TransactionModel.utime.label('timestamp'),
                                                msg_query.c.source,
                                                msg_query.c.destination,
                                                msg_query.c.value,
                                                TransactionModel.hash
                                            ).limit(page_size)\
                                             .offset(offset)\
                                             .all()

        return [
            {'Timestamp': t.timestamp, 'Source': t.source, 'Destination': t.destination,
             'Value': str(t.value / 100000000), 'Hash': t.hash} for t in transactions
        ]

    def get_grouped_transactions_by_address(self, address='', direction='send', page_num=1, page_size=100):
        if direction == 'Send':
            return [
                self._to_resp(r) 
                for r in MessageModel.get_transactions_grouped(address, '', '', page_num, page_size)
            ]
        else:
            return [
                self._to_resp(r) 
                for r in MessageModel.get_transactions_grouped('', address, '', page_num, page_size)
            ]

    def get_grouped_transactions_by_msg_hash(self, msg_hash=''):
        return [self._to_resp(r) for r in MessageModel.get_transactions_grouped('', '', msg_hash, 1, 1)]

    def _to_resp(self, record):
        return {
            'Source': record.source,
            'Destination': record.destination,
            'InTxCount': record.in_tx_cnt,
            "OutTxCount": record.out_tx_cnt,
            'Count': record.count,
            'TotalValue': str(record.total_value)
        }

    def get_grouped_transactions_by_tx_hash(self, tx_hash=''):
        tx_query = TransactionModel.query.filter(TransactionModel.hash == tx_hash)\
                                   .with_entities(TransactionModel.tx_id)\
                                   .subquery()\
                                   .alias('tx')

        record = MessageModel.query.session.query(tx_query)\
                             .outerjoin(MessageModel, MessageModel.in_tx_id == tx_query.c.tx_id)\
                             .group_by(
                                tx_query.c.tx_id,
                                MessageModel.source,
                                MessageModel.destination
                            )\
                             .with_entities(
                                    tx_query.c.tx_id,
                                    MessageModel.source,
                                    MessageModel.destination,
                                    func.count(distinct(MessageModel.in_tx_id)).label('in_tx_cnt'),
                                    func.count(distinct(MessageModel.out_tx_id)).label('out_tx_cnt'),
                                    func.sum(MessageModel.value).label('total_value'),
                            )\
                            .first()

        return [{
            'Source': record.source,
            'Destination': record.destination,
            "InTxCount": record.in_tx_cnt,
            "OutTxCount": record.out_tx_cnt,
            "Count": 1,
            "TotalValue": str(record.total_value / 100000000),
        }]

    def get_address_stats(self, address=''):
        resp = httpx.get(Config.TON_GET_ADDR_BALANCE, params={"address": address})
        if resp.status_code == 200:
            loaded = resp.json()
            total_balance = float(loaded['result']) / 100000000
        else:
            total_balance = 0

        # NOTE: Source => Outflow, Destination => Inflow
        outflow = MessageModel.get_address_total_value(address, '')
        inflow = MessageModel.get_address_total_value('', address)
        
        # TOP 5 Inflow & Outflow Addresses
        inflow_addrs = MessageModel.get_top_transaction_address(address, 'send', 1, 5)
        outflow_addrs = MessageModel.get_top_transaction_address(address, 'receive', 1, 5)

        return {
            'TotalBalance': str(total_balance),
            "TotalInflow": str(inflow.total_value / 100000000),
            "TotalOutflow": str(outflow.total_value / 100000000),
            "TOPInflow": [
                {"Address": i.address, "TotalValue": str(i.total_value),
                 "MsgCount": i.msg_cnt, "TxCount": i.tx_cnt}
                for i in inflow_addrs
            ],
            "TOPOutflow": [
                {"Address": o.address, "TotalValue": str(o.total_value),
                 "MsgCount": o.msg_cnt, "TxCount": o.tx_cnt}
                for o in outflow_addrs
            ],
        }
