from enum import Enum
from typing import Optional, Dict

from chainmodel.base_model import Block, Transaction, Log, Receipt, ChainData, EOAccount, Contract
from std_format import Hex


class EthereumTransactionType(Enum):
    # see https://eips.ethereum.org/EIPS/eip-1559
    Legacy  = 0
    EIP2930 = 1
    EIP1559 = 2

    @staticmethod
    def from_type_field(type_str: str):
        return EthereumTransactionType(Hex.hex_to_int(type_str))


class EthereumEOA(EOAccount):
    pass


class EthereumContract(Contract):
    pass


# noinspection PyUnresolvedReferences
class EthereumTransaction(Transaction):
    _Account_Cls  = EthereumEOA
    _Contract_Cls = EthereumContract

    _Attr_Handlers = {'from': ChainData._attr_ref_account,                      # uses default, always EOA account
                      'to': lambda self, *args: self._attr_ref_account(*args),  # can use override, e.g. EthereumTransaction
                      'type': lambda s, v, _: EthereumTransactionType.from_type_field(v),
                      'chainId': ChainData._attr_hex_to_int,
                      'input': ChainData._attr_hex_string,
                      }

    _Pretty_Suppress = {'blockHash', 'hash', 'r', 's', 'v'}

    def __init__(self, data_dict, fix_addresses=False):
        self.input = ''
        super().__init__(data_dict, fix_addresses)

    def assert_(self):
        super().assert_()
        assert isinstance(self.type, EthereumTransactionType)
        assert self.type == EthereumTransactionType.Legacy or (hasattr(self, 'chainId') and self.chainId == 1)

    @property
    def is_contract_call(self):
        return bool(self.input)

    # TODO
    # def is_contract_creation
    #     xxx

    def _attr_ref_account(self, address, fix_addresses):
        """ get/create the account and adds a cross-reference from the account to self
            - this version differentiates between contract and EOA accounts
        """
        cls = self._Contract_Cls if self.is_contract_call else self._Account_Cls
        acc = cls.add_xref(Hex.to_hex_addr(address) if fix_addresses else address, self)
        return self._attr_default_handler(acc, fix_addresses)


class EthereumLog(Log):
    _Attr_Handlers = {'data': ChainData._attr_hex_string}
    _Pretty_Suppress = {'blockHash', 'transactionHash'}


# noinspection PyUnresolvedReferences
class EthereumReceipt(Receipt):
    _Account_Cls = EthereumEOA

    _Attr_Handlers = {'from': ChainData._attr_ref_account,
                      'to': ChainData._attr_ref_account,
                      'type': lambda s, v, _: EthereumTransactionType.from_type_field(v),
                      'logs': Receipt._attr_init_logs,
                      }

    _Pretty_Suppress = {'blockHash', 'logsBloom', 'transactionHash'}

    def __init__(self, data_dict, fix_addresses=False):
        self.logs = None
        super().__init__(data_dict, fix_addresses)

    def assert_(self):
        super().assert_()
        assert isinstance(self.type, EthereumTransactionType)
        [log.assert_() for log in self.logs]


class EthereumBlock(Block):
    _Transaction_Cls = EthereumTransaction
    _Account_Cls = EthereumEOA

    _Attr_Handlers = {'transactions': Block._attr_init_transactions,
                      'miner': ChainData._attr_ref_account,
                      'nonce': ChainData._attr_hex_string,  # leave it a hex string
                      }

    _Pretty_Suppress = {'hash', 'logsBloom', 'mixHash', 'parentHash', 'receiptsRoot', 'sha3Uncles', 'stateRoot',
                        'transactionsRoot'}

    # def __init__(self, data_dict, fix_addresses=False):
    #     super().__init__(data_dict, fix_addresses)

    def assert_(self):
        # noinspection PyArgumentList
        super().assert_()
        [trans.assert_() for trans in self.transactions]

    def pretty(self, indent_level: int = 0, field_suppress: bool = False, pretty_fmt_override: Optional[Dict] = None):
        pretty_fmt_override = {
            EthereumTransaction: lambda v: v.pretty(indent_level + 1, field_suppress),
            **(pretty_fmt_override or {})
        }

        return super().pretty(indent_level, field_suppress, pretty_fmt_override)
