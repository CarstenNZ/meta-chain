from hexbytes import HexBytes
from std_format import Hex


class ChainData:
    _AttrHandlers = {}
    _TypeConverter = {
        HexBytes: lambda hb: Hex.fmt(hb.hex())
    }

    def __init__(self, block_dict):
        """ generic init crates instance attributes from dict items
            - 'Handler' class variable in derived classes can override this handling, e.g. create Transaction instances
              from the 'transaction' item
        """
        for k, v in block_dict.items():
            # noinspection PyArgumentList
            self.__class__._AttrHandlers.get(k, self.__class__.attr_default_handler)(self, k, v)

    def attr_default_handler(self, key, value):
        """ removes all special types, e.g. HexBytes from web3
        """
        if not isinstance(value, (int, str, list)):         # special type
            value = self._TypeConverter[type(value)](value)

        elif type(value) is str and Hex.isHexStr(value):    # std format for hex strings
            value = Hex.fmt(value)

        setattr(self, key, value)


class Transaction(ChainData):
    pass


class Block(ChainData):
    def __init__(self, block_dict):
        self.number = ""
        self.transactions = []
        super().__init__(block_dict)

    def _transactions(self, key, val):
        setattr(self, key, [Transaction(d) for d in val])

    _AttrHandlers = {'transactions': _transactions}
