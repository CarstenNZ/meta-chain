import unittest

from chainmodel.base import Block


# noinspection PyUnresolvedReferences
class TestChainModel(unittest.TestCase):
    # noinspection SpellCheckingInspection
    Block_dict = {'difficulty': '0x115f1167593b', 'extraData': '0xd783010305844765746887676f312e352e31856c696e7578',
                  'gasLimit': '0x47e7c4', 'gasUsed': '0xf618',
                  'hash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54',
                  'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000'
                               '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                               '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                               '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                               '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                               '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                               '0000000000000000000000',
                  'miner': '0x2a65aca4d5fc5b5c859090a6c34d164135398226',
                  'mixHash': '0xa85f3f580aba99dcf6ee9a2c8fe4c3b8094228e3ea62b8a483ac1ab9e3e43142',
                  'nonce': '0x8fad49e8b31d9c40', 'number': '0x123456',
                  'parentHash': '0x1f3a64ff24fbbc54504423c844ad75cc8e2572077d100b8ca0df6061a2618488',
                  'receiptsRoot': '0xbfab16d6510e2eb698b7824226ed04c562382b64bd2cfcdbc4a334848b66e51a',
                  'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
                  'size': '0x373',
                  'stateRoot': '0x4c7b0392cc6cc0e46f0bdd4254560e7f9553b10c06904747b091a4a958b58278',
                  'timestamp': '0x56f07dc7', 'totalDifficulty': '0x8dca5baa9b0198f9',
                  'transactions': [
                      {'blockHash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54',
                       'blockNumber': '0x123456', 'from': '0x2a65aca4d5fc5b5c859090a6c34d164135398226',
                       'gas': '0x15f90',
                       'gasPrice': '0x4a817c800',
                       'hash': '0xcb13faa6174ee9c1a21540cae32dd64ae6b3bc814b66ce5ed6843e65d112e391', 'input': '0x',
                       'nonce': '0x50640', 'to': '0xdbcbd5fc3693a8d6262b21376913c655d6e53c99',
                       'transactionIndex': '0x0',
                       'value': '0xe1134b1f1767400', 'type': '0x0', 'v': '0x1c',
                       'r': '0xcf2e63009fbc7439fc9e43fa332509c1a8cfb2c7f6fb34574c68f7ac8a74a82f',
                       's': '0x206bf09d62caa95b50aa3186195ab07133e32644292ad4fb005be783783c541a'},
                      {'blockHash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54',
                       'blockNumber': '0x123456', 'from': '0x151255dd9e38e44db38ea06ec66d0d113d6cbe37',
                       'gas': '0x15f90',
                       'gasPrice': '0x4a817c800',
                       'hash': '0x31c027886e28938ab21b8e371f3d3b3f3ff221b2786150b7e91d2bbdd69c4943', 'input': '0x',
                       'nonce': '0x2918', 'to': '0xa5ed89106ad81162f185e13b624838c693305a78', 'transactionIndex':
                           '0x1',
                       'value': '0xe10d76d29241800', 'type': '0x0', 'v': '0x1c',
                       'r': '0x6145dcd82fa305d654ba4058175945ad62d65eaceed3b332e18647252bad7bc1',
                       's': '0xaf780f675660426c459a52815f00a6774d325030b396dcdbf4f27279a63b41'},
                      {'blockHash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54',
                       'blockNumber': '0x123456', 'from': '0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98',
                       'gas': '0x5622',
                       'gasPrice': '0x4a817c800',
                       'hash': '0x02aea44c3af5b6398a27cf596abadae20a8e61ea37978d6b1bb0d6dec089a674', 'input': '0x',
                       'nonce': '0x2065', 'to': '0x6b3b2c3f961b2c3f2593338858ca89fa4c0ca247',
                       'transactionIndex': '0x2',
                       'value': '0x306ef8825a1d0000', 'type': '0x0', 'v': '0x1c',
                       'r': '0xb6d5df9df31ce28d9774542894a408c0e5fc553625e848cab6cc2acb12abbb8d',
                       's': '0x216f56b89c4b1b24104a8af78b89fedb47e0c16ff3cc24a96add4612ed741ce1'}
                  ],
                  'transactionsRoot': '0xe6f199ad7dff0523dab89a3d103afdf8bbaeabebc56fda6659876062dc361560',
                  'uncles': []}

    def test_createDataObjectFromDict(self):
        block = Block(self.Block_dict)
        assert len(block.transactions) == 3
        # noinspection SpellCheckingInspection
        assert block.transactions[2].hash == '0x02aea44c3af5b6398a27cf596abadae20a8e61ea37978d6b1bb0d6dec089a674'
        return block, self.Block_dict
