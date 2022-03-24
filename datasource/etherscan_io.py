from typing import Dict

import requests


class EtherscanIo:
    def __init__(self, service_endpoint, api_key):
        self.service_endpoint = service_endpoint
        self.api_key = api_key
        self.session = requests.Session()

    def get(self, module, action, extra_data='') -> Dict:
        """ request module/action/extra_data and return the result dict
        """
        url = f"{self.service_endpoint}?module={module}&action={action}&{extra_data}&apikey={self.api_key}"
        resp = self.session.get(url)
        if resp.status_code == 200:
            jContent = resp.json()
            if jContent['status'] == '1':
                return jContent['result']

        raise Exception(f"http request '{url}' failed with {resp.status_code}/'{resp.text}'")

    def __del__(self):
        self.session.close()