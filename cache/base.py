from abc import ABC, abstractmethod

from chainmodel.base import Block


class Cache(ABC):
    @abstractmethod
    def get_block(self, block_number: str):
        pass

    @abstractmethod
    def add_block(self, block: Block):
        pass

    @abstractmethod
    def close(self):
        pass