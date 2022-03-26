from typing import cast

from eth_typing import HexStr
from web3 import Web3

from chainmodel.base import Block
from datasource.base import DataSource
from std_format import Hex


class WebThree(DataSource):
    def __init__(self, service_endpoint: str):
        """
            - service_endpoint, e.g "https://mainnet.infura.io/v3/52754df7e5034e158acad0f5551e6eab"
        """
        self.w3 = Web3(Web3.HTTPProvider(service_endpoint))

    def get_block(self, block_number: str):
        block_number = Hex.fmt(block_number)
        return Block(self.w3.eth.get_block(cast(HexStr, block_number), full_transactions=True))

    def get_transaction_receipt(self, transaction_hash):
        breakpoint()
        # return Receipt(self.get('proxy', 'eth_getTransactionReceipt', txhash=txhash))

    def close(self):
        del self.w3
        self.w3 = None

    def __del__(self):
        self.close()
