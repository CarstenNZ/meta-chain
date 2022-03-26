import unittest

from cache.shelve import ShelveCache
from config import Config
from datasource.etherscan_io import EtherscanIo
from loader import Loader


class TestLoader(unittest.TestCase):
    dbPath = '/tmp/test.shelve'
    loader = None

    @classmethod
    def setUpClass(cls):
        config = Config.from_files(['~/meta-chain.yaml', '../meta-chain.yaml'])
        cache = ShelveCache(None, explicit_path=cls.dbPath, clear=True)
        eio = EtherscanIo(config)
        cls.loader = Loader([eio], cache)

    @classmethod
    def tearDownClass(cls):
        cls.loader.close()

    def test_basicLoaderTest(self):
        block1 = self.loader.get_block('0x123456')   # from data source
        block2 = self.loader.get_block('0x123456')   # from mem cache
        self.assertTrue(id(block1) == id(block2))

    def test_getReceipt(self):
        receipt = self.loader.get_transaction_receipt(
            '0xcb13faa6174ee9c1a21540cae32dd64ae6b3bc814b66ce5ed6843e65d112e391')
        assert receipt.blockHash == '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54'
