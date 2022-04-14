import os
import unittest

from cache.dbcache import DBCache
from chainmodel.base_model import Transaction
from chainmodel.ethereum_model import EthereumBlock
from config import Config
from tests.test_chainmodel import TestChainModelWithoutLoader


class TestDBCache(unittest.TestCase):
    def test_createShelfCache(self):
        config = Config(dict(cache=dict(path='/tmp/test.db')))
        block_dict = TestChainModelWithoutLoader.Block_dict
        block = EthereumBlock(block_dict)

        with DBCache(config, clear=True) as db:
            db.add_block(block, block_dict)

        with DBCache(config) as db:
            cache_block, _ = db.get_block(EthereumBlock, block.number)

        os.remove(config.get_cache_path())

        self.assertTrue(id(block) != id(cache_block))
        # noinspection PyUnresolvedReferences
        self.assertTrue(block.hash == cache_block.hash)
        self.assertTrue(isinstance(block.transactions[2], Transaction))
        self.assertTrue(block.transactions[2].hash == cache_block.transactions[2].hash)
