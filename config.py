import yaml

Default_Config_Paths = ('./meta-chain.yaml', '~/meta-chain.yaml')


class Config:
    def __init__(self, config_file_paths=Default_Config_Paths):
        for fp in config_file_paths:
            with open(fp, 'r') as f:
                self.tree = yaml.safe_load(f)
            return

        raise Exception(f"none of the config file found: {config_file_paths}")

    def get_etherscanIo_service(self):
        return self.get('datasource', 'etherscan.io', 'api_endpoint'), \
               self.get('datasource', 'etherscan.io', 'api_key')

    def get(self, *path, default=None):
        """ extract value at the end of path
            - returns default if path doesn't exist
        """
        node = self.tree
        for p in path:
            node = node.get(p, default)

        return node
