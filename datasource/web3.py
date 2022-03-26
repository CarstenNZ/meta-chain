from typing import cast

from eth_typing import HexStr
from hexbytes import HexBytes
from web3 import Web3

from chainmodel.base import Block, Receipt
from config import Config
from datasource.base import DataSource
from std_format import Hex


class WebThree(DataSource):
    _TypeConverter = {
        HexBytes: lambda h: Hex.fmt(h.hex()),
        list: lambda l: [WebThree._type_convert(i) for i in l],
        dict: lambda d: {k: WebThree._type_convert(v) for k, v in d.items()},
    }

    def __init__(self, config: Config):
        """
            - service_endpoint, e.g "https://mainnet.infura.io/v3/52754df7e5034e158acad0f5551e6eab"
        """
        self.w3 = Web3(Web3.HTTPProvider(config.get_web3_endpoint()))

    def get_block(self, block_number: int):
        block_src = self._type_convert(self.w3.eth.get_block(block_number, full_transactions=True))
        return Block(block_src), block_src

    def get_transaction_receipt(self, transaction_hash):
        receipt_src = self._type_convert(self.w3.eth.get_transaction_receipt(cast(HexStr, transaction_hash)))
        return Receipt(receipt_src), receipt_src

    def close(self):
        del self.w3
        self.w3 = None

    @classmethod
    def _type_convert(cls, data_dict):
        def convert_item(val):
            conv = cls._TypeConverter.get(type(val))
            return conv(val) if conv else val
        # <def

        return {k: convert_item(v) for k, v in data_dict.items()}

    def __del__(self):
        self.close()
