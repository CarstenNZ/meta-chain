import os
import unittest

from cache.shelvecache import ShelveCache
from chainmodel.base import Transaction
from config import Config
from tests.test_chainmodel import TestChainModel


class TestShelveCache(unittest.TestCase):
    def test_createShelfCache(self):
        config = Config(dict(cache=dict(path='/tmp/test.shelve')))
        block = TestChainModel().test_createDataObjectFromDict()

        with ShelveCache(config, clear=True) as db:
            db.add_block(block)

        with ShelveCache(config) as db:
            cache_block = db.get_block(block.number)

        os.remove(config.get_cache_path())

        self.assertTrue(id(block) != id(cache_block))
        self.assertTrue(block.hash == cache_block.hash)
        self.assertTrue(isinstance(block.transactions[2], Transaction))
        self.assertTrue(block.transactions[2].hash == cache_block.transactions[2].hash)
