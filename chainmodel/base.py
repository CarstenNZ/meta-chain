import yaml
from hexbytes import HexBytes
from std_format import Hex


class ChainData(yaml.YAMLObject):
    _AttrHandlers = {}
    _TypeConverter = {
        HexBytes: lambda hb: Hex.fmt(hb.hex())
    }

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
        if not isinstance(value, (int, str, list, type(None))):         # special type
            value = self._TypeConverter[type(value)](value)

        elif type(value) is str and Hex.isHexStr(value):    # std format for hex strings
            value = Hex.fmt(value)

        setattr(self, key, value)

    def pretty(self):
        """ return pretty formatted ChainData, multiline! yaml
        """
        return yaml.dump(self, indent=4)

    def __str__(self):
        return f"<{self.__class__.__name__}>"


class Transaction(ChainData):
    yaml_tag = '!Transaction'

    def __init__(self, data_dict):
        self.blockNumber = None
        self.transactionIndex = None
        super().__init__(data_dict)

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.blockNumber}/{self.transactionIndex}>"


class Receipt(ChainData):
    yaml_tag = '!Receipt'

    def __init__(self, data_dict):
        self.blockHash = None
        self.transactionHash = None
        super().__init__(data_dict)

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.transactionHash}>"


class Block(ChainData):
    yaml_tag = '!Block'

    def __init__(self, data_dict):
        self.transactions = []
        super().__init__(data_dict)

        # noinspection PyUnresolvedReferences
        self.number: int = self.number if isinstance(self.number, int) else int(self.number, 0)

    def _transactions(self, key, val):
        setattr(self, key, [Transaction(d) for d in val])

    def __str__(self):
        return f"<{self.__class__.__name__} #{self.number}>"

    _AttrHandlers = {'transactions': _transactions}
