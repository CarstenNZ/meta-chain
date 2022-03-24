from abc import ABC, abstractmethod

from chainmodel.base import Block


class DbCache(ABC):
    @abstractmethod
    def get_block(self, block_number):
        pass

    @abstractmethod
    def add_block(self, block: Block):
        pass

    @abstractmethod
    def close(self):
        pass