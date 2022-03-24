import unittest

from config import Config
from datasource.etherscan_io import EtherscanIo


class TestEtherscanIo(unittest.TestCase):
    def test_basicRequest(self):
        endpoint, key = Config(['../meta-chain.yaml']).get_etherscanIo_service()
        eio = EtherscanIo(endpoint, key)
        res = eio.get('stats', 'ethprice')

        assert {'ethbtc', 'ethusd'}.issubset(res.keys())
