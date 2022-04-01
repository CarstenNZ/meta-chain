import typing
from abc import ABC, abstractmethod
from typing import Optional, Dict, TypeVar

Account = TypeVar('Account')


class LoaderBase(ABC):
    """ all we need to use the 'with Loader...', but without the imports of the
        Loader implementation
    """
    _All_Accounts: Dict[str, Account] = {}

    # default loader is used for some get_.. methods if no explicit loader is provided
    # - not sure if we ever need multiple loaders, but it should be not too hard to implement
    #   them on this base
    Default_Loader: Optional['LoaderBase'] = None

    def __init__(self):
        # first loader becomes the default loader
        if LoaderBase.Default_Loader is None:
            LoaderBase.Default_Loader = self
            self._All_Accounts.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def get_account_name(cls, address):
        return cls.Default_Loader._get_account_name(address) if cls.Default_Loader else None

    @classmethod
    def get_account(cls, address):
        return cls._All_Accounts.get(address)

    @classmethod
    def add_account(cls, acc: Account) -> Account:
        assert acc.address not in cls._All_Accounts
        cls._All_Accounts[acc.address] = acc
        return acc

    @classmethod
    def all_accounts(cls) -> typing.ValuesView[Account]:
        return cls._All_Accounts.values()

    @abstractmethod
    def _get_account_name(self, address):
        pass

    def close(self):
        if LoaderBase.Default_Loader == self:
            LoaderBase.Default_Loader = None
            self._All_Accounts.clear()

