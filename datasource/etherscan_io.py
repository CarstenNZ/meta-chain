from typing import Dict

import requests


class EtherscanIo:
    def __init__(self, service_endpoint, api_key):
        self.service_endpoint = service_endpoint
        self.api_key = api_key
        self.session = requests.Session()

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

    def __del__(self):
        self.session.close()
