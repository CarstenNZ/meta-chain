import base64
from typing import List, Set, Any

from load.loaderbase import LoaderBase
from std_format import Hex


class ChainData:
    _AttrHandlers = {}

    def __init__(self, data_dict, fix_addresses=False):
        """ generic init crates instance attributes from dict items
            - 'Handler' class variable in derived classes can override this handling, e.g. create Transaction instances
              from the 'transaction' item
        """
        for key, val in data_dict.items():
            # noinspection PyArgumentList,PyNoneFunctionAssignment
            val = self.__class__._AttrHandlers.get(key, self.__class__.attr_default_handler)(self, val, fix_addresses)
            setattr(self, key, val)

    # noinspection PyMethodMayBeStatic
    def attr_default_handler(self, value: Any, _fix_addresses):
        return value

    def pretty(self, indent_level=0):
        """ return pretty formatted ChainData
        """
        new_line = '\n' + '\t' * (indent_level + 1)

        def fmt_value(value):
            return pretty_fmt.get(type(value), str)(value)

        def fmt_field(fld_name, value):
            return f"{fld_name}: {fmt_value(value)}"

        def fmt_list(list_):
            if not len(list_):
                return "[]"

            list_new_line = new_line + '\t'
            elements = list_new_line.join(fmt_value(i) for i in list_)
            return f"[{list_new_line}{elements}{new_line}]"

        # <def

        pretty_fmt = {
            int: lambda v: format(v, ','),
            str: lambda v: f"'{v}'",
            list: lambda v: fmt_list(v),
            # dict: lambda v: breakpoint(), # ">>>{v}<<<",
            Transaction: lambda v: v.pretty(indent_level + 2),
            Log: lambda v: v.pretty(indent_level + 2),
        }

        fields = new_line.join(fmt_field(k, v) for k, v in sorted(vars(self).items()))
        return f"{self}{new_line}{fields}"

    def _ref_account(self, address, fix_addresses):
        acc = Account.add_xref(Hex.to_hex_addr(address) if fix_addresses else address, self)
        return self.attr_default_handler(acc, fix_addresses)

    # noinspection PyMethodMayBeStatic
    def _hex_string(self, value, _fix_addresses):
        if Hex.is_hex(value):
            return value

        assert False

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class Account(ChainData):
    def __init__(self, address: str, name=None):
        assert Hex.is_hex_addr(address)

        super().__init__({})
        self.address = address
        self.name = name or Account._gen_default_name(address)
        self.xref: Set[ChainData] = set()

    @staticmethod
    def get_account(address) -> 'Account':
        """ returns Account for address
            - creates if it doesn't exist yet
        """
        assert Hex.is_hex_addr(address)
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

    @classmethod
    def _gen_default_name(cls, address):
        """ short name for account """
        return base64.b32encode(bytearray.fromhex(address[2:12])).decode()

    def __str__(self):
        return f"<{self.__class__.__name__} {self.name}/{self.address}>"


class Transaction(ChainData):
    _AttrHandlers = {'from': ChainData._ref_account,
                     'to': ChainData._ref_account,
                     'type': ChainData._hex_string,
                     'input': ChainData._hex_string,
                     }

    def __init__(self, data_dict, fix_addresses=False):
        self.hash = ''
        super().__init__(data_dict, fix_addresses)

    def get_receipt(self, loader=None):
        assert (loader or LoaderBase.Default_Loader), "needs explicit loader argument or active (default) Loader"
        return (loader or LoaderBase.Default_Loader).get_transaction_receipt(self.hash)

    def __str__(self):
        try:
            # noinspection PyUnresolvedReferences
            return f"<{self.__class__.__name__} #{self.blockNumber:,}/{self.transactionIndex:,}>"
        except AttributeError:
            return f"<{self.__class__.__name__}>"


class Log(ChainData):
    _AttrHandlers = {'data': ChainData._hex_string,
                     }

    def __str__(self):
        try:
            # noinspection PyUnresolvedReferences
            return f"<{self.__class__.__name__} #{self.blockNumber:,}/{self.transactionIndex:,}/{self.logIndex:,}>"
        except AttributeError:
            return f"<{self.__class__.__name__}>"


class Receipt(ChainData):
    def __init__(self, data_dict, fix_addresses=False):
        self.transactionHash = None
        self.blockNumber = -1
        self.transactionIndex = -1
        super().__init__(data_dict, fix_addresses)

    # noinspection PyUnresolvedReferences
    def get_transaction(self, loader=None):
        assert (loader or LoaderBase.Default_Loader), "needs explicit loader argument or active (default) Loader"
        block = (loader or LoaderBase.Default_Loader).get_block(self.blockNumber)
        return block.transactions[self.transactionIndex]

    # noinspection PyMethodMayBeStatic
    def _init_logs(self, val, _fix_addresses):
        return [Log(d) for d in val]

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.blockNumber:,}/{self.transactionIndex:,}>"

    _AttrHandlers = {'from': ChainData._ref_account,
                     'to': ChainData._ref_account,
                     'type': ChainData._hex_string,
                     'logs': _init_logs,
                     }


class Block(ChainData):
    # noinspection PyUnresolvedReferences
    def __init__(self, data_dict, fix_addresses=False):
        self.number = -1
        self.transactions: List[Transaction] = []
        super().__init__(data_dict, fix_addresses=fix_addresses)

    # noinspection PyMethodMayBeStatic
    def _init_transactions(self, val, fix_addresses):
        return [Transaction(d, fix_addresses) for d in val]

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.number:,}>"

    _AttrHandlers = {'transactions': _init_transactions,
                     'miner': ChainData._ref_account,
                     'nonce': ChainData._hex_string,              # leave it a hex string
                     }
