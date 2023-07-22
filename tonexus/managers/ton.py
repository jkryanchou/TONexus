# -*- coding=utf-8 -*-

from tonexus.managers.base import Singleton
from tonexus.models import (
    Message as MessageModel,
    Transaction as TransactionModel,
)
from tonexus.utils import print_raw_sql


class TONManager(Singleton):

    def get_transactions_between_accounts(self, sender='', receiver='', page_num=1, page_size=10):
        return [
            {'Source': r.source, 'Destination': r.destination, 'Count': r.count} 
            for r in MessageModel.get_transactions_accounts(sender, receiver, '', page_num, page_size)
        ]

    def get_transactions_graph_by_account(self, account='', direction='send', page_num=1, page_size=10):
        if direction == 'send':
            return [
                {'Source': r.source, 'Destination': r.destination, 'Count': r.count}
                for r in MessageModel.get_transactions_accounts(account, '', '', page_num, page_size)
            ]
        else:
            return [
                {'Source': r.source, 'Destination': r.destination, 'Count': r.count}
                for r in MessageModel.get_transactions_accounts('', account, '', page_num, page_size)
            ]

    def get_transactions_graph_by_msg_hash(self, msg_hash=''):
        return [
            {'Source': r.source, 'Destination': r.destination}
            for r in MessageModel.get_transactions_accounts('', '', msg_hash, 1, 1)
        ]

    def get_transactions_graph_by_tx_hash(self, tx_hash=''):
        tx_query = TransactionModel.query.filter(TransactionModel.hash == tx_hash)\
                                   .with_entities(TransactionModel.tx_id)\
                                   .subquery()\
                                   .alias('tx')

        record = MessageModel.query.session.query(tx_query)\
                             .outerjoin(MessageModel, MessageModel.in_tx_id == tx_query.c.tx_id)\
                             .with_entities(MessageModel.source, MessageModel.destination)\
                             .first()

        return [{'Source': record.source, 'Destination': record.destination}]

    def get_account_stats(self, account_address=''):
        pass

    def get_transaction_stats(self, account_address=''):
        pass

    def evaluate_account_or_transaction(self, query=''):
        pass

    # def get_account_transaction_addresses(self, account_address='', direction='in',  page_num=1, page_size=10):
    #     pass
