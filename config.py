from pathlib import Path

import yaml

Default_Config_Paths = ('./meta-chain.yaml', '~/meta-chain.yaml')


class Config:
    def __init__(self, config_file_paths=Default_Config_Paths):
        for fp in config_file_paths:
            try:
                with open(Path(fp).expanduser(), 'r') as f:
                    self.tree = yaml.safe_load(f)
                return
            except FileNotFoundError:
                pass

        raise Exception(f"none of the config file found: {config_file_paths}")

    def get_etherscanIo_service(self):
        esNode = self.get('datasource', 'etherscan.io')
        return esNode['api_endpoint'], esNode['api_key']

    def get(self, *path, default=None):
        """ extract value at the end of path
            - returns default if path doesn't exist
        """
        node = self.tree
        for p in path:
            node = node.get(p, default)

        return node
