import unittest
from pathlib import Path

from cache.shelvecache import ShelveCache
from config import Config
from datasource.etherscan_io import EtherscanIo
from datasource.web3 import WebThree
from load.loader import Loader
from std_format import Hex


class TestLoader(unittest.TestCase):
    dbDirectory = Path('/tmp')
    loaders = {}

    @classmethod
    def setUpClass(cls):
        config = Config.from_files(['~/meta-chain.yaml', '../meta-chain.yaml'])
        cls.loaders = {'ethereum.io': Loader([EtherscanIo(config)],
                                             ShelveCache(None, explicit_path=cls.dbDirectory / 'eioCache.shelve',
                                                         clear=True)),
                       'web3': Loader([WebThree(config)],
                                      ShelveCache(None, explicit_path=cls.dbDirectory / 'webCache.shelve', clear=True))
                       }

    @classmethod
    def tearDownClass(cls):
        [ld.close() for ld in cls.loaders.values()]

    def test_basicLoaderTest(self):
        for name, loader in self.loaders.items():
            block1 = loader.get_block(0x123456)   # from data source
            block2 = loader.get_block(0x123456)   # from mem cache
            self.assertTrue(id(block1) == id(block2))

    # noinspection PyUnresolvedReferences
    def test_getReceipt(self):
        for name, loader in self.loaders.items():
            receipt = loader.get_transaction_receipt(
                '0xcb13faa6174ee9c1a21540cae32dd64ae6b3bc814b66ce5ed6843e65d112e391')
            assert receipt.blockHash == '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54'

    def test_getCode(self):
        loader = self.loaders['web3']
        code = loader.get_code('0x514910771AF9Ca656af840dff83E8264EcF986CA')

        self.assertTrue(Hex.is_hex_addr(code.address))
        self.assertTrue(sum(code.bytes) == 274930)
