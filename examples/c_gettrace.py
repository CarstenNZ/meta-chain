""" dig into transaction as described here
        https://www.trustology.io/insights-events/decoding-an-ethereum-transaction-its-no-secret-its-just-smart
        - transaction "0xdadd97094b8a789d387a53845449d52213e9ffd37a3530d8d99d2234dea820fa" in block 10879272
"""

from pathlib import Path

from cache.dbcache import DBCache
from config import Config
from datasource.etherscan_io import EtherscanIo
from datasource.web3 import *
from load.loader import Loader
from utils.helpers import first

CONFIG_PATHS = ['~/meta-chain.yaml',  # your copy with api keys, not part of project
                '../meta-chain.yaml'  # example config
                ]


# noinspection SpellCheckingInspection
def main():
    # find a config file
    config = Config.from_files(CONFIG_PATHS)

    # create loader, ! this will fail without valid api keys in your config
    data_source = EtherscanIo(config) # use WebThree(config) or EtherscanIo(config)
    with Loader([data_source], DBCache(config, explicit_path='/tmp/web3.cache.db'),
                Path('../tests/data/known_accounts.yaml')) as loader:

        # get some transaction details
        block = loader.get_block(10879272)
        transaction = first(t for t in block.transactions if t.hash == "0xdadd97094b8a789d387a53845449d52213e9ffd37a3530d8d99d2234dea820fa")
        receipt = transaction.get_receipt()
        assert transaction.transactionIndex == 107

        method = transaction.input[:4]


        # _t = loader.get_trace("0x2059dd53ecac9827faad14d364f9e04b1d5fe5b506e3acc886eff7a6f88a696a")
        breakpoint()


if __name__ == '__main__':
    main()
