from chainmodel.base_model import Block, Transaction, Log, Receipt, ChainData, Account, Code


class EthereumAccount(Account):
    pass


class EthereumCode(Code):
    pass


class EthereumTransaction(Transaction):
    _Account_Cls = EthereumAccount

    _Attr_Handlers = {'from': ChainData._ref_account,
                      'to': ChainData._ref_account,
                      'type': ChainData._hex_string,
                      'input': ChainData._hex_string,
                      }

    _Pretty_Suppress = {'blockHash', 'hash', 'r', 's', 'v'}


class EthereumLog(Log):
    _Attr_Handlers = {'data': ChainData._hex_string}
    _Pretty_Suppress = {'blockHash', 'transactionHash'}


class EthereumReceipt(Receipt):
    _Account_Cls = EthereumAccount
    _Pretty_Suppress = {'blockHash', 'logsBloom', 'transactionHash'}


class EthereumBlock(Block):
    _Transaction_Cls = EthereumTransaction
    _Account_Cls = EthereumAccount

    _Attr_Handlers = {'transactions': Block._init_transactions,
                      'miner': ChainData._ref_account,
                      'nonce': ChainData._hex_string,  # leave it a hex string
                      }

    _Pretty_Suppress = {'hash', 'logsBloom', 'mixHash', 'parentHash', 'receiptsRoot', 'sha3Uncles', 'stateRoot',
                        'transactionsRoot'}
