import unittest

from config import Config
from datasource.web3 import WebThree


class TestWeb3(unittest.TestCase):
    w3 = None

    @classmethod
    def setUpClass(cls):
        config = Config.from_files(['~/meta-chain.yaml', '../meta-chain.yaml'])
        cls.w3 = WebThree(config)

    @classmethod
    def tearDownClass(cls):
        cls.w3.close()

    def test_blockRequest(self):
        block, block_src = self.w3.get_block(0x123456)
        # noinspection PyUnresolvedReferences
        assert block.extraData == '0xd783010305844765746887676f312e352e31856c696e7578'

