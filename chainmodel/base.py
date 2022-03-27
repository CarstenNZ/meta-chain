import base64
from typing import List, Dict, Set

import yaml

from load.loaderbase import LoaderBase
from std_format import Hex


class ChainData(yaml.YAMLObject):
    _AttrHandlers = {}

    def __init__(self, data_dict):
        """ generic init crates instance attributes from dict items
            - 'Handler' class variable in derived classes can override this handling, e.g. create Transaction instances
              from the 'transaction' item
        """
        for k, v in data_dict.items():
            # noinspection PyArgumentList
            self.__class__._AttrHandlers.get(k, self.__class__.attr_default_handler)(self, k, v)

    def attr_default_handler(self, key, value):
        """ removes all special types, e.g. HexBytes from web3
        """
        if type(value) is str and Hex.isHexStr(value):    # std format for hex strings
            value = Hex.fmt(value)

        setattr(self, key, value)

    def pretty(self):
        """ return pretty formatted ChainData, multiline! yaml
        """
        return yaml.dump(self, indent=4)

    def _ref_account(self, _field, address):
        Account.add_xref(address, self)

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class Account(ChainData):
    All_Accounts: Dict[str, 'Account'] = {}

    def __init__(self, address: str):
        assert Hex.isHexStr(address)

        super().__init__({})
        self.address = address
        self.xref: Set[ChainData] = set()

    @property
    def name(self):
        """ short name for account """
        return base64.b32encode(bytearray.fromhex(self.address[2:12])).decode()

    @staticmethod
    def add_xref(address: str, ref_data: ChainData):
        address = Hex.fmt(address)
        acc = Account.All_Accounts.get(address)
        if acc is None:
            Account.All_Accounts[Hex.fmt(address)] = acc = Account(address)

        acc.xref.add(ref_data)
        return acc

    def __str__(self):
        return f"<{self.__class__.__name__} {self.address}>"


class Transaction(ChainData):
    _AttrHandlers = {'from': ChainData._ref_account,
                     'to': ChainData._ref_account}

    def __init__(self, data_dict):
        self.hash = ''
        self.blockNumber = -1
        self.transactionIndex = -1
        super().__init__(data_dict)

    def get_receipt(self, loader=None):
        assert (loader or LoaderBase.Default_Loader), "needs explicit loader argument or active (default) Loader"
        return (loader or LoaderBase.Default_Loader).get_transaction_receipt(self.hash)

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.blockNumber}/{self.transactionIndex}>"


class Receipt(ChainData):
    _AttrHandlers = {'from': ChainData._ref_account,
                     'to': ChainData._ref_account}

    def __init__(self, data_dict):
        self.transactionHash = None
        super().__init__(data_dict)

    # noinspection PyUnresolvedReferences
    def get_transaction(self, loader=None):
        assert (loader or LoaderBase.Default_Loader), "needs explicit loader argument or active (default) Loader"
        block = (loader or LoaderBase.Default_Loader).get_block(self.blockNumber)
        return block.transactions[self.transactionIndex]

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.transactionHash}>"


class Block(ChainData):
    # noinspection PyUnresolvedReferences
    def __init__(self, data_dict):
        self.number = -1
        self.transactions: List[Transaction] = []
        super().__init__(data_dict)

    def _init_transactions(self, key, val):
        setattr(self, key, [Transaction(d) for d in val])

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.number}>"

    _AttrHandlers = {'transactions': _init_transactions,
                     'miner': ChainData._ref_account}
