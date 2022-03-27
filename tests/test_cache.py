import os
import unittest

from cache.shelvecache import ShelveCache
from chainmodel.base import Transaction, Block
from config import Config
from tests.test_chainmodel import TestChainModelWithoutLoader


class TestShelveCache(unittest.TestCase):
    def test_createShelfCache(self):
        config = Config(dict(cache=dict(path='/tmp/test.shelve')))
        block_src = TestChainModelWithoutLoader.Block_dict
        block = Block(block_src)

        with ShelveCache(config, clear=True) as db:
            db.add_block(block, block_src)

        with ShelveCache(config) as db:
            cache_block, _ = db.get_block(block.number)

        os.remove(config.get_cache_path())

        self.assertTrue(id(block) != id(cache_block))
        # noinspection PyUnresolvedReferences
        self.assertTrue(block.hash == cache_block.hash)
        self.assertTrue(isinstance(block.transactions[2], Transaction))
        self.assertTrue(block.transactions[2].hash == cache_block.transactions[2].hash)
