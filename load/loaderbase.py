from abc import ABC
from typing import Optional


class LoaderBase(ABC):
    """ all we need to use the 'with Loader...', but without the imports of the
        Loader implementation
    """

    # default loader is used for some get_.. methods if no explicit loader is provided
    Default_Loader: Optional['LoaderBase'] = None

    def __init__(self):
        # first loader becomes the default loader
        if LoaderBase.Default_Loader is None:
            LoaderBase.Default_Loader = self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if LoaderBase.Default_Loader == self:
            LoaderBase.Default_Loader = None

