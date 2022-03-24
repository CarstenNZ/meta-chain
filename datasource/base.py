from abc import ABC, abstractmethod


class DataSource(ABC):
    """ abstract base class for all data sources
    """

    @abstractmethod
    def loadBlock(self, block_number):
        pass