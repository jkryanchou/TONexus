# -*- coding=utf-8 -*-

from tests.factories.base import BaseFactory
from tonexus.models import Message, Transaction


class MessageFactory(BaseFactory):

    class Meta:
        model = Message


class TransactionFactory(BaseFactory):

    class Meta:
        model = Transaction
