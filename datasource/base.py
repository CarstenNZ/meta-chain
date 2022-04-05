from abc import ABC, abstractmethod
from typing import Tuple

from chainmodel.base import Block, Receipt


class DataSource(ABC):
    """ abstract base class for all data sources
    """

    @abstractmethod
    def get_block(self, block_number: int) -> Tuple[Block, str]:
        pass

    @abstractmethod
    def get_transaction_receipt(self, transaction_hash) -> Tuple[Receipt, str]:
        pass

    @abstractmethod
    def get_code(self, contract_address):
        pass

    @abstractmethod
    def close(self):
        pass