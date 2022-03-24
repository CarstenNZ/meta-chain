import unittest

from cache.shelve import ShelveCache
from config import Config
from datasource.etherscan_io import EtherscanIo
from loader import Loader


class TestLoader(unittest.TestCase):

    def test_basicLoaderTest(self):
        dbPath = '/tmp/test.shelve'
        endpoint, key = Config(['~/meta-chain.yaml', '../meta-chain.yaml']).get_etherscanIo_service()
        loader = Loader([EtherscanIo(endpoint, key)], ShelveCache(dbPath, clear=True))

        block1 = loader.get_block('0x123456')   # from data source
        block2 = loader.get_block('0x123456')   # from mem cache
        self.assertTrue(id(block1) == id(block2))

        # new loader with same DB will load from DB, but the block will be a different instance
        loader.close()
        loader = Loader([EtherscanIo(endpoint, key)], ShelveCache(dbPath))
        block3 = loader.get_block('0x123456')   # from DB
        self.assertTrue(id(block3) != id(block2))
