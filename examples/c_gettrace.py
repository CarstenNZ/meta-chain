from pathlib import Path

from cache.dbcache import DBCache
from config import Config
# from datasource.etherscan_io import EtherscanIo
from datasource.web3 import WebThree
from load.loader import Loader

CONFIG_PATHS = ['~/meta-chain.yaml',  # your copy with api keys, not part of project
                '../meta-chain.yaml'  # example config
                ]


# noinspection SpellCheckingInspection
def main():
    # find a config file
    config = Config.from_files(CONFIG_PATHS)

    # create loader, ! this will fail without valid api keys in your config
    data_source = WebThree(config)  # or use EtherscanIo(config)
    with Loader([data_source], DBCache(config, explicit_path='/tmp/web3.cache.db'),
                Path('../tests/data/known_accounts.yaml')) as loader:

        # traces = []
        # for transact in block.transactions:
        #     if transact.is_contract_call:
        #         t = loader.get_trace("0x2059dd53ecac9827faad14d364f9e04b1d5fe5b506e3acc886eff7a6f88a696a")
        #         break

        _t = loader.get_trace("0x2059dd53ecac9827faad14d364f9e04b1d5fe5b506e3acc886eff7a6f88a696a")
        breakpoint()


if __name__ == '__main__':
    main()
