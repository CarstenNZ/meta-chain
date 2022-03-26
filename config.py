from pathlib import Path
from typing import Dict

import yaml

Default_Config_Paths = ('./meta-chain.yaml', '~/meta-chain.yaml')


class Config:
    def __init__(self, config_tree: Dict):
        self.tree = config_tree

    @staticmethod
    def from_files(config_file_paths=Default_Config_Paths):
        for fp in config_file_paths:
            try:
                with open(Path(fp).expanduser(), 'r') as f:
                    return Config(yaml.safe_load(f))
            except FileNotFoundError:
                pass

        raise Exception(f"none of the config file found: {config_file_paths}")

    def get_cache_path(self):
        return self.get('cache', 'path')

    def get_etherscanIo_service(self):
        esNode = self.get('datasource', 'etherscan.io')
        return esNode['api_endpoint'], esNode['api_key']

    def get_web3_endpoint(self):
        return self.get('datasource', 'web3', 'api_endpoint')

    def get(self, *path, default=None):
        """ extract value at the end of path
            - returns default if path doesn't exist
        """
        node = self.tree
        for p in path:
            node = node.get(p, default)

        return node
