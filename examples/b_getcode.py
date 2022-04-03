from pathlib import Path

from cache.shelvecache import ShelveCache
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
    with Loader([data_source], ShelveCache(config, explicit_path='/tmp/web3.shelve'),
                Path('../tests/data/known_accounts.yaml')) as loader:

        # load block
        block = loader.get_block(10_000_000)   # loaded from persistent cache or data source

        # pretty output
        print(block.pretty())

        for transact in block.transactions:
            receipt = loader.get_transaction_receipt(transact.hash)
            print(receipt.pretty())


if __name__ == '__main__':
    main()
