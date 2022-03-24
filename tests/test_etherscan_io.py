import unittest

from config import Config
from datasource.etherscan_io import EtherscanIo


class TestEtherscanIo(unittest.TestCase):
    eio = None

    @classmethod
    def setUpClass(cls):
        endpoint, key = Config(['~/meta-chain.yaml', '../meta-chain.yaml']).get_etherscanIo_service()
        cls.eio = EtherscanIo(endpoint, key)

    @classmethod
    def tearDownClass(cls):
        cls.eio.close()

    def test_basicRequest(self):
        res = self.eio.get('stats', 'ethprice')
        assert {'ethbtc', 'ethusd'}.issubset(res.keys())

    def test_blockRequest(self):
        res = self.eio.get('proxy', 'eth_getBlockByNumber', tag='0x123456', boolean='true')
        assert res['extraData'] == '0xd783010305844765746887676f312e352e31856c696e7578'

