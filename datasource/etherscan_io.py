from typing import Dict

import requests

from chainmodel.base import Block
from config import Config
from datasource.base import DataSource
from std_format import Hex


class EtherscanIo(DataSource):
    def __init__(self, config: Config):
        endpoint, key = config.get_etherscanIo_service()

        self.service_endpoint = endpoint
        self.api_key = key
        self.session = requests.Session()

    def get_block(self, block_number: str):
        block_number = Hex.fmt(block_number)
        return Block(self.get('proxy', 'eth_getBlockByNumber', tag=block_number, boolean='true'))

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

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

    def __del__(self):
        self.close()
