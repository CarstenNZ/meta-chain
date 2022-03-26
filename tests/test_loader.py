import unittest

from cache.shelve import ShelveCache
from config import Config
from datasource.etherscan_io import EtherscanIo
from loader import Loader


class TestLoader(unittest.TestCase):

    def test_basicLoaderTest(self):
        dbPath = '/tmp/test.shelve'
        config = Config.from_files(['~/meta-chain.yaml', '../meta-chain.yaml'])
        loader = Loader([EtherscanIo(config)], ShelveCache(None, explicit_path=dbPath, clear=True))

        block1 = loader.get_block('0x123456')   # from data source
        block2 = loader.get_block('0x123456')   # from mem cache
        self.assertTrue(id(block1) == id(block2))

        # new loader with same DB will load from DB, but the block will be a different instance
        loader.close()
        loader = Loader([EtherscanIo(config)], ShelveCache(None, explicit_path=dbPath))
        block3 = loader.get_block('0x123456')   # from DB
        self.assertTrue(id(block3) != id(block2))
