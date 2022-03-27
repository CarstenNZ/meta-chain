from abc import ABC, abstractmethod
from typing import Optional


class LoaderBase(ABC):
    """ all we need to use the 'with Loader...', but without the imports of the
        Loader implementation
    """

    Default_Loader: Optional['LoaderBase'] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.Default_Loader == self:
            self.Default_Loader = None

        self.close()

    @abstractmethod
    def close(self):
        pass