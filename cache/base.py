from abc import abstractmethod

from chainmodel.base import Block, Receipt
from datasource.base import DataSource


class Cache(DataSource):
    """ Cache is just a data source, but also needs add_... methods
    """

    @abstractmethod
    def add_block(self, block: Block):
        pass

    @abstractmethod
    def add_transaction_receipt(self, receipt: Receipt):
        pass
