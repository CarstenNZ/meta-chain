from abc import ABC, abstractmethod
from typing import Tuple

from chainmodel.base_model import Block, Receipt


class DataSource(ABC):
    """ abstract base class for all data sources
    """

    @abstractmethod
    def get_block(self, block_cls, block_number: int) -> Tuple[Block, str]:
        pass

    @abstractmethod
    def get_transaction_receipt(self, receipt_cls, transaction_hash) -> Tuple[Receipt, str]:
        pass

    @abstractmethod
    def get_code(self, contract_cls, contract_address):
        pass

    @abstractmethod
    def close(self):
        pass