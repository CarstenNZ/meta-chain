
from cache.shelve import ShelveCache
from config import Config
from datasource.etherscan_io import EtherscanIo
from loader import Loader

CONFIG_PATHS = ['~/meta-chain.yaml',  # your copy with api keys, not part of project
                '../meta-chain.yaml'  # example config
                ]


def main():
    # find a config file
    config = Config.from_files(CONFIG_PATHS)

    # create loader, this will fail without api keys in your config
    loader = Loader([EtherscanIo(config)], ShelveCache(config))

    # load the same block twice
    block1 = loader.get_block('0x123456')   # loaded from persistent cache or data source
    block2 = loader.get_block('0x123456')   # loaded from mem cache

    # same python object
    assert id(block1) == id(block2)

    # pretty output
    print(block1.pretty_str())


if __name__ == '__main__':
    main()

