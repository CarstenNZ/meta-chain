from abc import ABC, abstractmethod


class DataSource(ABC):
    """ abstract base class for all data sources
    """

    @abstractmethod
    def get_block(self, block_number):
        pass

    @abstractmethod
    def get_transaction_receipt(self, transaction_hash):
        pass

    @abstractmethod
    def close(self):
        pass