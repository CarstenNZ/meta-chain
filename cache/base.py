from abc import abstractmethod

from chainmodel.base_model import Block, Receipt, Contract
from datasource.base import DataSource


class Cache(DataSource):
    """ Cache is just a data source, but also needs add_... methods
    """

    @abstractmethod
    def add_block(self, block: Block, block_dict: dict):
        pass

    @abstractmethod
    def add_transaction_receipt(self, receipt: Receipt, receipt_src: str):
        pass

    @abstractmethod
    def add_code(self, code: Contract, code_bytes: str):
        pass

