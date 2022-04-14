from typing import cast

from eth_typing import HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3.datastructures import AttributeDict

from config import Config
from datasource.base import DataSource
from std_format import Hex


class WebThree(DataSource):
    _TypeConverter = {
        HexBytes: lambda h: Hex.fmt(h.hex()),
        list: lambda l: [WebThree._convert_item(i) for i in l],
        dict: lambda d: {k: WebThree._convert_item(v) for k, v in d.items()},
        AttributeDict: lambda d: {k: WebThree._convert_item(v) for k, v in d.items()},
    }

    def __init__(self, config: Config):
        """
            - service_endpoint, e.g "https://mainnet.infura.io/v3/52754df7e5034e158acad0f5551e6eab"
        """
        self.w3 = Web3(Web3.HTTPProvider(config.get_web3_endpoint(), request_kwargs={'timeout': 30}))

    def get_block(self, block_cls, block_number: int):
        block_src = self._convert_item(self.w3.eth.get_block(block_number, full_transactions=True))
        return block_cls(block_src), block_src

    def get_transaction_receipt(self, receipt_cls, transaction_hash):
        receipt_src = self._convert_item(self.w3.eth.get_transaction_receipt(cast(HexStr, transaction_hash)))
        return receipt_cls(receipt_src), receipt_src

    def get_code(self, code_cls, contract_address):
        code_bytes = self._convert_item(self.w3.eth.get_code(cast(HexStr, contract_address)))
        return code_cls(contract_address, code_bytes), code_bytes

    def get_transaction_trace(self, trace_cls, transaction_address):
        trace_str = self._convert_item(self.w3.manager.request_blocking('debug_traceTransaction', [transaction_address]))
        return trace_cls(transaction_address, trace_str), trace_str

    def close(self):
        del self.w3
        self.w3 = None

    @classmethod
    def _convert_item(cls, val):
        conv = cls._TypeConverter.get(type(val))
        return conv(val) if conv else val

    def __del__(self):
        self.close()
