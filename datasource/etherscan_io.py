from typing import Dict

import requests

from chainmodel.base import Block, Receipt
from config import Config
from datasource.base import DataSource
from std_format import Hex


class EtherscanIo(DataSource):
    Transaction_Converter = {
        'type': lambda v: v,
        'value': lambda v: int(v, 16),
    }

    Block_Converter = {
        'totalDifficulty': lambda v: int(v, 16),
        'transactions': lambda v: [EtherscanIo._fix_itemTypes(e, EtherscanIo.Transaction_Converter) for e in v]
    }

    Receipt_Converter = {
        'type': lambda v: v,
    }

    def __init__(self, config: Config):
        endpoint, key = config.get_etherscanIo_service()

        self.service_endpoint = endpoint
        self.api_key = key
        self.session = requests.Session()

    def get_block(self, block_number: int):
        data_dict = self.get('proxy', 'eth_getBlockByNumber', tag=hex(block_number), boolean='true')
        return Block(self._fix_itemTypes(data_dict, EtherscanIo.Block_Converter))

    def get_transaction_receipt(self, transaction_hash):
        data_dict = self.get('proxy', 'eth_getTransactionReceipt', txhash=transaction_hash)
        return Receipt(self._fix_itemTypes(data_dict, EtherscanIo.Receipt_Converter))

    def get(self, module, action, **kwargs) -> Dict:
        """ request module/action/**kwargs and return the result dict
        """
        extra_data = '&' + '&'.join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ''
        url = f"{self.service_endpoint}?module={module}&action={action}{extra_data}&apikey={self.api_key}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            jContent = resp.json()
            if module == 'proxy' or jContent.get('status') == '1':    # no status in proxy requests
                return jContent['result']

        raise Exception(f"http request '{url}' failed with {resp.status_code}/'{resp.text}'")

    @staticmethod
    def _fix_itemTypes(data_dict: Dict, converter: Dict):
        """ data types are often different from web3, so we fix them here
        """
        def fix_item(key, val):
            # explicit
            conv = converter.get(key)
            if conv:
                return conv(val)

            # short hex become int
            if isinstance(val, str) and Hex.isHexStr(val) and len(val) < 2 + 16:
                return int(val, 16)

            return val
        # < def

        return {key: fix_item(key, val) for key, val in data_dict.items()}

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

    def __del__(self):
        self.close()
