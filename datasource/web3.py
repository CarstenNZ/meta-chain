from typing import cast

from eth_typing import HexStr
from web3 import Web3

from chainmodel.base import Block, Receipt
from config import Config
from datasource.base import DataSource


class WebThree(DataSource):
    def __init__(self, config: Config):
        """
            - service_endpoint, e.g "https://mainnet.infura.io/v3/52754df7e5034e158acad0f5551e6eab"
        """
        self.w3 = Web3(Web3.HTTPProvider(config.get_web3_endpoint()))

    def get_block(self, block_number: int):
        block_src = self.w3.eth.get_block(block_number, full_transactions=True)
        return Block(block_src), block_src

    def get_transaction_receipt(self, transaction_hash):
        receipt_src = self.w3.eth.get_transaction_receipt(cast(HexStr, transaction_hash))
        return Receipt(receipt_src), receipt_src

    def close(self):
        del self.w3
        self.w3 = None

    def __del__(self):
        self.close()
