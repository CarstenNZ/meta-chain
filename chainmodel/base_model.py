import base64
from typing import List, Set, Any

from load.loaderbase import LoaderBase
from std_format import Hex


class ChainData:
    _Account_Cls = None

    _Attr_Handlers = {}
    _Pretty_Suppress = set()

    def __init__(self, data_dict, fix_addresses=False):
        """ generic init crates instance attributes from dict items
            - 'Handler' class variable in derived classes can override this handling, e.g. create Transaction instances
              from the 'transaction' item
        """
        for key, val in data_dict.items():
            # noinspection PyArgumentList,PyNoneFunctionAssignment
            val = self.__class__._Attr_Handlers.get(key, self.__class__.attr_default_handler)(self, val, fix_addresses)
            setattr(self, key, val)

    # noinspection PyMethodMayBeStatic
    def attr_default_handler(self, value: Any, _fix_addresses):
        return value

    def pretty(self, indent_level: int = 0, field_suppress: bool = False):
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
            Transaction: lambda v: v.pretty(indent_level + 2, field_suppress),
            Log: lambda v: v.pretty(indent_level + 2, field_suppress),
        }

        fields = new_line.join(fmt_field(k, v) for k, v in sorted(vars(self).items())
                               if field_suppress is False or k not in self._Pretty_Suppress)
        return f"{self}{new_line}{fields}"

    def _ref_account(self, address, fix_addresses):
        acc = self._Account_Cls.add_xref(Hex.to_hex_addr(address) if fix_addresses else address, self)
        return self.attr_default_handler(acc, fix_addresses)

    # noinspection PyMethodMayBeStatic
    def _hex_string(self, value, _fix_addresses):
        if Hex.is_hex(value):
            return value if len(value) > 2 else ''

        assert False

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class Transaction(ChainData):
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

    _Attr_Handlers = {'from': ChainData._ref_account,
                      'to': ChainData._ref_account,
                      'type': ChainData._hex_string,
                      'logs': _init_logs,
                      }


class Account(ChainData):
    def __init__(self, address: str, name=None):
        assert Hex.is_hex_addr(address)

        super().__init__({})
        self.address = address
        self.name = name or self._gen_default_name(address)
        self.xref: Set[ChainData] = set()

    @classmethod
    def get_account(cls, address) -> 'Account':
        """ returns Account for address
            - creates if it doesn't exist yet
        """
        assert Hex.is_hex_addr(address)
        acc = LoaderBase.get_account(address)
        if acc is None:
            name = LoaderBase.get_account_name(address)
            acc = LoaderBase.add_account(cls(address, name))

        return acc

    @classmethod
    def add_xref(cls, address: str, ref_data: ChainData) -> 'Account':
        acc = cls.get_account(address)

        acc.xref.add(ref_data)
        return acc

    @classmethod
    def _gen_default_name(cls, address, prefix='@'):
        """ short name for account
        """
        return prefix + base64.b32encode(bytearray.fromhex(address[2:12])).decode()

    def __str__(self):
        return f"<{self.__class__.__name__} {self.name}/{self.address}>"


class Code(Account):
    def __init__(self, code_address, code_bytes_str):
        self.address = None
        super().__init__(code_address)

        Hex.is_hex(code_bytes_str)
        self.bytes = bytearray.fromhex(code_bytes_str[2:])

    @classmethod
    def _gen_default_name(cls, address, prefix='x'):
        """ short name for account
        """
        return super()._gen_default_name(address, prefix)


class Block(ChainData):
    _Account_Cls = Account
    _Transaction_Cls = Transaction

    # noinspection PyUnresolvedReferences
    def __init__(self, data_dict, fix_addresses=False):
        self.number = -1
        self.transactions: List[Transaction] = []
        super().__init__(data_dict, fix_addresses=fix_addresses)

    # noinspection PyMethodMayBeStatic
    def _init_transactions(self, val, fix_addresses):
        return [self._Transaction_Cls(d, fix_addresses) for d in val]

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.number:,}>"



