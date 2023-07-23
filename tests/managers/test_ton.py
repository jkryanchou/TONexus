# -*- coding=utf-8 -*-

from tonexus.managers import TONManager
from tests.managers.base import BaseManagerTestCase

# NOTE: Do not run the unnitest due to lack of integrating with the local PostgreSQL database.
# The database was highly integrated with ton-indexer(https://github.com/toncenter/ton-indexer)

class TestTONManager(BaseManagerTestCase):

    def setUp(self):
        self._manager = TONManager()
        super(TestTONManager, self).setUp()

    def test_get_grouped_transactions_by_sender_should_be_correct(self):
        sender = '0:f66c656e08f41e3227e2587c79e378d5cd0558d42e076785f59e907c49b872b3'
        page_num, page_size = 1, 10
        txns = self._manager.get_grouped_transactions_by_address(sender, 'send', page_num, page_size)
        assert len(txns) == 10
        for t in txns:
            assert t['Source'] == sender

    def test_get_grouped_transactions_by_receiver_should_be_correct(self):
        receiver = '0:f66c656e08f41e3227e2587c79e378d5cd0558d42e076785f59e907c49b872b3'
        page_num, page_size = 1, 10
        txns = self._manager.get_grouped_transactions_by_address(
            receiver, 'receive', page_num, page_size
        )
        assert len(txns) == 10
        for t in txns:
            assert t['Destination'] == receiver

    def test_get_grouped_transactions_between_addresses_should_be_correct(self):
        sender = '0:5239b71ac50e62c577e626cc12af146b08b64a4e2e9718fd459c2300e5b205bd'
        receiever = '0:310b71b340182396f5ba08903081a1ef6ab4df571a3ca7b05effa44c4a3b0f92'
        page_num, page_size = 1, 10
        txns = self._manager.get_transactions_between_addresses(
            sender, receiever, page_num, page_size
        )

        for t in txns:
            assert t['Destination'] == receiever
            assert t['Source'] == sender

    def test_get_grouped_transactions_by_msg_hash_should_be_correct(self):
        # TODO: Refactor to Local Test
        msg_hash = 'l2qL1RtlS/HMbXnZOiIaOTHF8SGmsIS5TslDz6XXxpg='
        txns = self._manager.get_grouped_transactions_by_msg_hash(msg_hash)

        assert len(txns) == 1

    def test_get_transactions_graph_by_tx_hash_should_be_correct(self):
        # TODO: Refactor to Local Test
        tx_hash = 'AnXpweO4HggoaDHDD5e76gHMj7dqHatQOpkdkvzwf/Q='
        txns = self._manager.get_grouped_transactions_by_tx_hash(tx_hash)

        assert len(txns) == 1

    def test_get_account_stats_should_be_correct(self):
        addr = '0:ea33d122cd0784393b6b7f348263775e340d9ac464c5107b943014f6e402f12f'
        stats = self._manager.get_address_stats(addr)

        assert set(stats.keys()) == {
            'TotalBalance', 'TotalInflow', 'TotalOutflow',
            "TOPInflow", "TOPOutflow"
        }

    def test_get_transactions_between_addresses_should_be_correct(self):
        '''
        -1:16d6f0a9035b6bf71afa4125d2c5c552767d529bb4985ff3c259074295a5a16a, 0:a44757069a7b04e393782b4a2d3e5e449f19d16a4986a9e25436e6b97e45a16a
        '''

        sender, receiever = '-1:16d6f0a9035b6bf71afa4125d2c5c552767d529bb4985ff3c259074295a5a16a', '0:a44757069a7b04e393782b4a2d3e5e449f19d16a4986a9e25436e6b97e45a16a'
        transactions = self._manager.get_transactions_between_addresses(sender, receiever, 1, 10)
        assert transactions[0]['Source'] == sender
        assert transactions[0]['Destination'] == receiever
