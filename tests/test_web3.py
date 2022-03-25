import unittest

from config import Config
from datasource.web3 import WebThree


class TestWeb3(unittest.TestCase):
    w3 = None

    @classmethod
    def setUpClass(cls):
        endpoint = Config(['~/meta-chain.yaml', '../meta-chain.yaml']).get_web3_endpoint()
        cls.w3 = WebThree(endpoint)

    @classmethod
    def tearDownClass(cls):
        cls.w3.close()

    def test_blockRequest(self):
        block = self.w3.get_block('0x123456')
        assert block.extraData == '0xd783010305844765746887676f312e352e31856c696e7578'

