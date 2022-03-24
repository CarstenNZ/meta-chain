
class ChainData:
    AttrHandler = {}

    def __init__(self, block_dict):
        """ generic init crates instance attributes from dict items
            - 'Handler' class variable in derived classes can override this handling, e.g. create Transaction instances
              from the 'transaction' item
        """
        for k, v in block_dict.items():
            self.__class__.AttrHandler.get(k, setattr)(self, k, v)


class Transaction(ChainData):
    pass


class Block(ChainData):
    def _transactions(self, key, val):
        setattr(self, key, [Transaction(d) for d in val])

    AttrHandler = {'transactions': _transactions}
