# -*- coding=utf-8 -*-

from flask import Blueprint

from tonexus.response import write_json
from tonexus.decorators import require_params
from tonexus import schemas
from tonexus.managers import TONManager


TONEXUS_BP = Blueprint("tonexus", __name__)


@TONEXUS_BP.route("/ListGroupedTransactionsByAddress", methods=["GET"])
@require_params(schemas.ListGroupedTransactionsByAddressSchema, position="query")
def list_grouped_transactions_by_address(args):
    manager = TONManager()
    txns = manager.get_grouped_transactions_by_address(
        args['address'], args['direction'], args['page_num'], args['page_size']
    )
    return write_json(txns)


@TONEXUS_BP.route("/ListGroupedTransactionsByTXHash", methods=["GET"])
@require_params(schemas.ListGroupedTransactionsByTXHashSchema, position="query")
def list_grouped_transactions_by_tx_hash(args):
    manager = TONManager()
    txns = manager.get_grouped_transactions_by_tx_hash(args["hash"])
    return write_json(txns)


@TONEXUS_BP.route("/ListGroupedTransactionsByMsgHash", methods=["GET"])
@require_params(schemas.ListGroupedTransactionsByMsgHashSchema, position="query")
def list_grouped_transactions_by_msg_hash(args):
    manager = TONManager()
    txns = manager.get_grouped_transactions_by_msg_hash(args["hash"])
    return write_json(txns)


@TONEXUS_BP.route("/ListTransactionsBetweenAddresses", methods=["GET"])
@require_params(schemas.ListTransactionsBetweenAddresses, position="query")
def list_transactions_between_addresses(args):
    manager = TONManager()
    txns = manager.get_transactions_between_addresses(args["source"], args["destination"])
    return write_json(txns)


@TONEXUS_BP.route("/GetAddressStats", methods=["GET"])
@require_params(schemas.GetAddressStats, position="query")
def get_address_stats(args):
    manager = TONManager()
    stats = manager.get_address_stats(args['address'])
    return write_json(stats)
