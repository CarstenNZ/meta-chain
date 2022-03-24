import os
import unittest

from cache.shelve import ShelveCache
from chainmodel.base import Transaction
from tests.test_chainmodel import TestChainModel


class TestShelveCache(unittest.TestCase):
    def test_createShelfCache(self):
        dbPath = '/tmp/test.shelve'
        block = TestChainModel().test_createDataObjectFromDict()

        with ShelveCache(dbPath, clear=True) as db:
            db.add_block(block)

        with ShelveCache(dbPath) as db:
            cache_block = db.get_block(block.number)

        os.remove(dbPath)

        self.assertTrue(id(block) != id(cache_block))
        self.assertTrue(block.hash == cache_block.hash)
        self.assertTrue(isinstance(block.transactions[2], Transaction))
        self.assertTrue(block.transactions[2].hash == cache_block.transactions[2].hash)
