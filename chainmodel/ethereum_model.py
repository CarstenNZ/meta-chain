from chainmodel.base_model import Block, Transaction, Log, Receipt


class EthereumTransaction(Transaction):
    pass


class EthereumLog(Log):
    pass


class EthereumReceipt(Receipt):
    pass


class EthereumBlock(Block):
    _Transaction_Cls = EthereumTransaction
    pass