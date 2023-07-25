# -*- coding=utf-8 -*-

from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Index, Enum, func, desc, distinct
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY

from tonexus.ext import db
from tonexus.utils import print_raw_sql


# NOTE: The models was migreate from the ton-indexer project (ref: https://github.com/toncenter/ton-indexer/blob/master/indexer/database.py)
# TODO: Refactor the models to support the local test

@dataclass(init=False)
class Block(db.Model):

    __tablename__ = 'blocks'

    block_id: int = Column(Integer, autoincrement=True, primary_key=True)
    workchain: int = Column(Integer, nullable=False)
    shard: int = Column(BigInteger)
    seqno: int = Column(Integer)
    root_hash: str = Column(String(44))
    file_hash: str = Column(String(44))
    masterchain_block_id = Column(Integer, ForeignKey('blocks.block_id'))

    shards = relationship("Block",
        backref=backref('masterchain_block', remote_side=[block_id])
    )

    __table_args__ = (Index('blocks_index_1', 'workchain', 'shard', 'seqno'),
                      Index('blocks_index_2', 'masterchain_block_id'),
                      UniqueConstraint('workchain', 'shard', 'seqno'))


@dataclass(init=False)
class BlockHeader(db.Model):

    __tablename__ = 'block_headers'
    
    block_id: int = Column(Integer, ForeignKey('blocks.block_id'), primary_key=True)
    global_id: int = Column(Integer)
    version: int = Column(Integer)
    flags: int = Column(Integer)
    after_merge: bool = Column(Boolean)
    after_split: bool = Column(Boolean)
    before_split: bool = Column(Boolean)
    want_merge: bool = Column(Boolean)
    validator_list_hash_short: int = Column(Integer)
    catchain_seqno: int = Column(Integer)
    min_ref_mc_seqno: int = Column(Integer)
    is_key_block: bool = Column(Boolean)
    prev_key_block_seqno: int = Column(Integer)
    start_lt: int = Column(BigInteger)
    end_lt: int = Column(BigInteger)
    gen_utime: int = Column(BigInteger)
    vert_seqno: int = Column(Integer)
    
    block = relationship("Block", backref=backref("block_header", uselist=False))

    __table_args__ = (Index('block_headers_index_1', 'catchain_seqno'), 
                      Index('block_headers_index_2', 'min_ref_mc_seqno'),
                      Index('block_headers_index_3', 'prev_key_block_seqno'),
                      Index('block_headers_index_4', 'start_lt', 'end_lt'),
                      Index('block_headers_index_5', 'is_key_block'),
                      Index('block_headers_index_6', 'gen_utime'))


@dataclass(init=False)
class Transaction(db.Model):

    __tablename__ = 'transactions'
    
    tx_id: int = Column(BigInteger, autoincrement=True, primary_key=True)
    account: str = Column(String)
    account_code_hash: str = Column(String)
    account_code_hash_rel = relationship(
        'CodeHashInterfaces', foreign_keys=[account_code_hash],
        primaryjoin='CodeHashInterfaces.code_hash == Transaction.account_code_hash'
    )
    lt: int = Column(BigInteger)
    hash: str = Column(String(44))
    balance: int = Column(BigInteger)
    utime: int = Column(BigInteger)
    fee: int = Column(BigInteger)
    storage_fee: int = Column(BigInteger)
    other_fee: int = Column(BigInteger)
    transaction_type = Column(Enum('trans_storage', 'trans_ord', 'trans_tick_tock', 
                                   'trans_split_prepare', 'trans_split_install', 
                                   'trans_merge_prepare', 'trans_merge_install', 
                                   name='trans_type'))
    compute_exit_code: int = Column(Integer)
    compute_gas_used: int = Column(Integer)
    compute_gas_limit: int = Column(Integer)
    compute_gas_credit: int = Column(Integer)
    compute_gas_fees: int = Column(BigInteger)
    compute_vm_steps: int = Column(Integer)
    compute_skip_reason: str = Column(Enum(
        'cskip_no_state', 'cskip_bad_state', 'cskip_no_gas', name='compute_skip_reason_type'
    ))
    action_result_code: int = Column(Integer)
    action_total_fwd_fees: int = Column(BigInteger)
    action_total_action_fees: int = Column(BigInteger)
    block_id = Column(Integer, ForeignKey("blocks.block_id"))
    block = relationship("Block", backref="transactions")
    in_msg = relationship("Message", uselist=False, back_populates="in_tx", foreign_keys="Message.in_tx_id")
    out_msgs = relationship("Message", back_populates="out_tx", foreign_keys="Message.out_tx_id")

    __table_args__ = (Index('transactions_index_1', 'account'),
                      Index('transactions_index_2', 'utime'), 
                      Index('transactions_index_3', 'hash'),
                      Index('transactions_index_4', 'lt'),
                      Index('transactions_index_5', 'account', 'utime'),
                      Index('transactions_index_6', 'block_id'))


@dataclass(init=False)
class Message(db.Model):

    __tablename__ = 'messages'

    msg_id: int = Column(BigInteger, primary_key=True)
    source: str = Column(String)
    destination: str = Column(String)
    value: int = Column(BigInteger)
    fwd_fee: int = Column(BigInteger)
    ihr_fee: int = Column(BigInteger)
    created_lt: int = Column(BigInteger)
    hash: str = Column(String(44))
    body_hash: str = Column(String(44))
    op: int = Column(Integer)
    comment: str = Column(String)
    ihr_disabled: bool = Column(Boolean)
    bounce: bool = Column(Boolean)
    bounced: bool = Column(Boolean)
    has_init_state: bool = Column(Boolean)
    import_fee: int = Column(BigInteger)
    
    out_tx_id = Column(BigInteger, ForeignKey("transactions.tx_id"))
    out_tx = relationship("Transaction", back_populates="out_msgs", foreign_keys=[out_tx_id])

    in_tx_id = Column(BigInteger, ForeignKey("transactions.tx_id"))
    in_tx = relationship("Transaction", back_populates="in_msg", 
                        uselist=False, foreign_keys=[in_tx_id])

    __table_args__ = (Index('messages_index_1', 'source'),
                      Index('messages_index_2', 'destination'),
                      Index('messages_index_3', 'created_lt'),
                      Index('messages_index_4', 'hash'),
                      Index('messages_index_5', 'body_hash'),
                      Index('messages_index_6', 'source', 'destination', 'created_lt'),
                      Index('messages_index_7', 'in_tx_id'),
                      Index('messages_index_8', 'out_tx_id'))

    @classmethod
    def get_transactions_grouped(cls, source='', destination='', msg_hash='',
                                  page_num=1, page_size=100):
        offset = (page_num - 1) * page_size
        query = cls.query.with_entities(cls.source,
                                        cls.destination,
                                        func.count(cls.msg_id).label('count'),
                                        func.count(distinct(cls.in_tx_id)).label('in_tx_cnt'),
                                        func.count(distinct(cls.out_tx_id)).label('out_tx_cnt'),
                                        (func.sum(cls.value) / 100000000).label('total_value'))

        if source:
            query = query.filter(cls.source == source)

        if destination:
            query = query.filter(cls.destination == destination)

        if msg_hash:
            query = query.filter(cls.hash == msg_hash)

        grouped_query = query.group_by(cls.source, cls.destination)\
                             .order_by(desc('count'))\
                             .limit(page_size)\
                             .offset(offset)
                            #  .all()

        # print_raw_sql(grouped_query)

        return grouped_query.all()

    @classmethod
    def get_address_total_value(cls, source='', destination=''):
        query = cls.query
        if source:
            query = query.filter(cls.source == source)

        if destination:
            query = query.filter(cls.destination == destination)

        result = query.group_by(cls.source)\
                      .with_entities(func.sum(cls.value).label('total_value'))\
                      .first()
        return result

    @classmethod
    def get_top_transaction_address(cls, addr='', direction='send', page_num=1, page_size=100):
        # FIX: Total Value should not be minus
        offset = (page_num - 1) * page_size

        if direction == 'send':
            return cls.query.filter(cls.source == addr)\
                      .with_entities(
                         cls.destination.label('address'),
                         func.sum(cls.value / 100000000).label('total_value'),
                         func.count(distinct(cls.out_tx_id)).label('tx_cnt'),
                         func.count(cls.msg_id).label('msg_cnt'),
                       )\
                       .group_by(cls.destination)\
                       .order_by(desc('total_value'))\
                       .limit(page_size)\
                       .offset(offset)\
                       .all()

        # direction = Receive
        else:
            return cls.query.filter(cls.destination == addr)\
                      .with_entities(
                         cls.source.label('address'),
                         func.sum(cls.value / 100000000).label('total_value'),
                         func.count(distinct(cls.in_tx_id)).label('tx_cnt'),
                         func.count(cls.msg_id).label('msg_cnt'),
                       )\
                       .group_by(cls.source)\
                       .order_by(desc('total_value'))\
                       .limit(page_size)\
                       .offset(offset)\
                       .all()


@dataclass(init=False)
class MessageContent(db.Model):

    __tablename__ = 'message_contents'

    msg_id: int = Column(BigInteger, ForeignKey("messages.msg_id"), primary_key=True)
    body: str = Column(String)
    msg = relationship("Message", backref=backref(
        "content", cascade="save-update, merge, delete, delete-orphan", uselist=False
    ))


class CodeHashInterfaces(db.Model):

    __tablename__ = 'code_hash'

    code_hash = Column(String, primary_key=True)
    interfaces = Column(ARRAY(Enum('nft_item', 
                                   'nft_editable', 
                                   'nft_collection', 
                                   'nft_royalty',
                                   'jetton_wallet', 
                                   'jetton_master',
                                   'domain',
                                   'subscription',
                                   'auction',
                                   name='interface_name')))
