from typing import List, Set

from load.loaderbase import LoaderBase
from std_format import Hex


class ChainData:
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
        if type(value) is str and Hex.isHexStr(value):  # std format for hex strings
            value = Hex.fmt(value)

        setattr(self, key, value)

    def pretty(self):
        """ return pretty formatted ChainData
        """

        def fmt_field(fld_name, value):
            return f"{fld_name}: {pretty_fmt[type(value)](value)}"

        def fmt_list(list_):
            elements = "\n\t".join(str(i) for i in list_)
            return f"[\n\t{elements}]"

        pretty_fmt = {
            str: lambda v: f"'{v}'",
            int: lambda v: f"{v}",
            list: lambda v: fmt_list(v),
            type(None): lambda v: "None"
        }

        fields = "\n\t".join(fmt_field(k, v) for k, v in sorted(vars(self).items()))
        return f"{self.__class__.__name__}\n\t{fields}"

    def _ref_account(self, field, address):
        Account.add_xref(address, self)
        self.attr_default_handler(field, address)

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class Account(ChainData):
    def __init__(self, address: str, name=None):
        assert Hex.isHexStr(address)

        super().__init__({})
        self.address = address
        self.name = name
        self.xref: Set[ChainData] = set()

    # @property
    # def name(self):
    #     """ short name for account """
    #     return base64.b32encode(bytearray.fromhex(self.address[2:12])).decode()

    @staticmethod
    def get_account(address) -> 'Account':
        """ returns Account for address
            - creates if it doesn't exist yet
        """
        address = Hex.fmt(address)
        acc = LoaderBase.get_account(address)
        if acc is None:
            name = LoaderBase.get_account_name(address)
            acc = LoaderBase.add_account(Account(address, name))

        return acc

    @staticmethod
    def add_xref(address: str, ref_data: ChainData) -> 'Account':
        acc = Account.get_account(address)

        acc.xref.add(ref_data)
        return acc

    def __str__(self):
        name = (self.name + '/') if self.name else ''
        return f"<{self.__class__.__name__} {name}{self.address}>"


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
