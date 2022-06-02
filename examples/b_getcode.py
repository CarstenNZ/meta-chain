from pathlib import Path
from typing import cast

from cache.dbcache import DBCache
from chainmodel.ethereum_model import EthereumBlock
from config import Config
from datasource.etherscan_io import EtherscanIo
from datasource.web3 import WebThree
from load.loader import Loader

CONFIG_PATHS = ['~/meta-chain.yaml',  # your copy with api keys, not part of project
                '../meta-chain.yaml'  # example config
                ]


def main():
    # find a config file
    config = Config.from_files(CONFIG_PATHS)

    # create loader, ! this will fail without valid api keys in your config
    data_source = WebThree(config)  # or use EtherscanIo(config)
    with Loader([data_source], DBCache(config, explicit_path='/tmp/web3.cache.db'),
                Path('../tests/data/known_accounts.yaml')) as loader:
        # load block
        block = cast(EthereumBlock, loader.get_block(14_000_000))  # loaded from persistent cache or data source
        block.assert_()
        print(block.pretty(field_suppress=True))

        for transact in block.transactions:
            receipt = loader.get_transaction_receipt(transact.hash)
            receipt.assert_()
            print(receipt.pretty(field_suppress=True))

        # active accounts, sorted by cross-references
        accounts = sorted(Loader.all_accounts(), key=lambda a: -len(a.xref))
        print("\nAccounts\n\t" + "\n\t".join(f"{a.address}, xRefs {len(a.xref)}" for a in accounts))

        # contract code
        codes = [loader.get_code(transact.to.address) for transact in block.transactions if transact.is_contract_call]
        print("\nContract codes\n\t" + "\n\t".join(f"{c.address}, len {len(c.bytes)}" for c in codes))


if __name__ == '__main__':
    main()
