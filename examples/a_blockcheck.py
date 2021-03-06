from pathlib import Path

from cache.dbcache import DBCache
from config import Config
# from datasource.etherscan_io import EtherscanIo
from datasource.web3 import WebThree
from load.loader import Loader

CONFIG_PATHS = ['~/meta-chain.yaml',  # your copy with api keys, not part of project
                '../meta-chain.yaml'  # example config
                ]


def main():
    # find a config file
    config = Config.from_files(CONFIG_PATHS)

    # create loader, this will fail without api keys in your config
    data_source = WebThree(config)      # or use EtherscanIo(config)
    with Loader([data_source], DBCache(config, explicit_path='/tmp/0x123456.cache.db'),
                Path('../tests/data/known_accounts.yaml')) as loader:

        # load the same block twice
        block1 = loader.get_block(0x123456)   # loaded from persistent cache or data source
        block2 = loader.get_block(0x123456)   # loaded from mem cache

        # same python object
        assert id(block1) == id(block2)

        # pretty output
        print(block1.pretty())

        for transact in block1.transactions:
            receipt = loader.get_transaction_receipt(transact.hash)
            print(receipt.pretty())


if __name__ == '__main__':
    main()
