from chainmodel.base_model import Block, Transaction, Log, Receipt, ChainData, Account, Code


class EthereumAccount(Account):
    pass


class EthereumCode(Code):
    pass


class EthereumTransaction(Transaction):
    _Account_Cls = EthereumAccount

    _Attr_Handlers = {'from': ChainData._attr_ref_account,
                      'to': ChainData._attr_ref_account,
                      'type': ChainData._attr_hex_string,
                      'input': ChainData._attr_hex_string,
                      }

    _Pretty_Suppress = {'blockHash', 'hash', 'r', 's', 'v'}


class EthereumLog(Log):
    _Attr_Handlers = {'data': ChainData._attr_hex_string}
    _Pretty_Suppress = {'blockHash', 'transactionHash'}


class EthereumReceipt(Receipt):
    _Account_Cls = EthereumAccount

    _Attr_Handlers = {'from': ChainData._attr_ref_account,
                      'to': ChainData._attr_ref_account,
                      'type': ChainData._attr_hex_string,
                      'logs': Receipt._attr_init_logs,
                      }

    _Pretty_Suppress = {'blockHash', 'logsBloom', 'transactionHash'}

    def __init__(self, data_dict, fix_addresses=False):
        self.logs = None
        super().__init__(data_dict, fix_addresses)

    def assert_(self):
        super().assert_()
        [log.assert_() for log in self.logs]


class EthereumBlock(Block):
    _Transaction_Cls = EthereumTransaction
    _Account_Cls = EthereumAccount

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
