import unittest

from config import Config
from cache.shelvecache import ShelveCache
from loader.loader import Loader
from chainmodel.base import Block, Account


# noinspection PyUnresolvedReferences
class TestChainModelWithoutLoader(unittest.TestCase):
    # noinspection SpellCheckingInspection
    Block_dict = {
        'difficulty': 19100011551035, 'extraData': '0xd783010305844765746887676f312e352e31856c696e7578',
        'gasLimit': 4712388, 'gasUsed': 63000,
        'hash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54',
        'logsBloom': '0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                     '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                     '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                     '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                     '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                     '0000000000000000000000000000000000000000000000000000000000000000',
        'miner': '0x2a65Aca4D5fC5B5C859090a6c34d164135398226',
        'mixHash': '0xa85f3f580aba99dcf6ee9a2c8fe4c3b8094228e3ea62b8a483ac1ab9e3e43142',
        'nonce': '0x8fad49e8b31d9c40', 'number': 1193046,
        'parentHash': '0x1f3a64ff24fbbc54504423c844ad75cc8e2572077d100b8ca0df6061a2618488',
        'receiptsRoot': '0xbfab16d6510e2eb698b7824226ed04c562382b64bd2cfcdbc4a334848b66e51a',
        'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347', 'size': 883,
        'stateRoot': '0x4c7b0392cc6cc0e46f0bdd4254560e7f9553b10c06904747b091a4a958b58278',
        'timestamp': 1458601415, 'totalDifficulty': 10217079492946532601, 'transactions': [
            {'blockHash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54', 'blockNumber': 1193046,
             'from': '0x2a65Aca4D5fC5B5C859090a6c34d164135398226', 'gas': 90000, 'gasPrice': 20000000000,
             'hash': '0xcb13faa6174ee9c1a21540cae32dd64ae6b3bc814b66ce5ed6843e65d112e391', 'input': '0x',
             'nonce': 329280, 'r': '0xcf2e63009fbc7439fc9e43fa332509c1a8cfb2c7f6fb34574c68f7ac8a74a82f',
             's': '0x206bf09d62caa95b50aa3186195ab07133e32644292ad4fb005be783783c541a',
             'to': '0xdBcbd5fc3693a8D6262b21376913c655D6E53C99', 'transactionIndex': 0, 'type': '0x0', 'v': 28,
             'value': 1013649330000000000},
            {'blockHash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54', 'blockNumber': 1193046,
             'from': '0x151255dD9E38e44DB38EA06EC66D0D113D6cBe37', 'gas': 90000, 'gasPrice': 20000000000,
             'hash': '0x31c027886e28938ab21b8e371f3d3b3f3ff221b2786150b7e91d2bbdd69c4943', 'input': '0x',
             'nonce': 10520, 'r': '0x6145dcd82fa305d654ba4058175945ad62d65eaceed3b332e18647252bad7bc1',
             's': '0xaf780f675660426c459a52815f00a6774d325030b396dcdbf4f27279a63b41',
             'to': '0xa5Ed89106aD81162F185E13B624838C693305A78', 'transactionIndex': 1, 'type': '0x0', 'v': 28,
             'value': 1013546780000000000},
            {'blockHash': '0xb5e7f8b71f2ea15f001634a9f7657cd35d29898d56de57663de0e7ebc15b7b54', 'blockNumber': 1193046,
             'from': '0xFBb1b73C4f0BDa4f67dcA266ce6Ef42f520fBB98', 'gas': 22050, 'gasPrice': 20000000000,
             'hash': '0x02aea44c3af5b6398a27cf596abadae20a8e61ea37978d6b1bb0d6dec089a674', 'input': '0x', 'nonce': 8293,
             'r': '0xb6d5df9df31ce28d9774542894a408c0e5fc553625e848cab6cc2acb12abbb8d',
             's': '0x216f56b89c4b1b24104a8af78b89fedb47e0c16ff3cc24a96add4612ed741ce1',
             'to': '0x6B3B2c3F961b2c3F2593338858CA89fa4c0Ca247', 'transactionIndex': 2, 'type': '0x0', 'v': 28,
             'value': 3490000000000000000}],
        'transactionsRoot': '0xe6f199ad7dff0523dab89a3d103afdf8bbaeabebc56fda6659876062dc361560',
        'uncles': []
    }

    def test_createDataObjectFromDict(self):
        block = Block(self.Block_dict)
        assert len(block.transactions) == 3
        # noinspection SpellCheckingInspection
        assert block.transactions[2].hash == '0x02aea44c3af5b6398a27cf596abadae20a8e61ea37978d6b1bb0d6dec089a674'

        # The block didn't go through the cache, but is reachable via Account.All_Accounts (xref).
        # This breaks the order for the following tests, so we have to clean up to avoid this.
        Account.All_Accounts.clear()

        return block, self.Block_dict


class TestChainModel0x123456(unittest.TestCase):

    # noinspection PyUnresolvedReferences
    @classmethod
    def setUpClass(cls):
        Account.All_Accounts.clear()        # needs clear slate
        config = Config.from_files(['data/0x123456-tests.yaml'])
        cls.loader = Loader([], ShelveCache(config))
        cls.block = cls.loader.get_block(0x123456)
        cls.receipts = [cls.loader.get_transaction_receipt(transact.hash) for transact in cls.block.transactions]

    @classmethod
    def tearDownClass(cls):
        Account.All_Accounts.clear()

    def test_relatedAccounts(self):
        """ check accounts collected from block 0x123456 are stable
        """

        accountStrs = [f'{acc}: {sorted(str(r) for r in acc.xref)}' for acc in
                       sorted(Account.All_Accounts.values(), key=lambda a: a.address)]

        # noinspection SpellCheckingInspection
        expectedAccountStr = [
            "<Account 0x151255dd9e38e44db38ea06ec66d0d113d6cbe37>: ['<Receipt #0x31c027886e28938ab21b8e371f3d3b3f3ff221b2786150b7e91d2bbdd69c4943>', '<Transaction #1193046/1>']",
            "<Account 0x2a65aca4d5fc5b5c859090a6c34d164135398226>: ['<Block #1193046>', '<Receipt #0xcb13faa6174ee9c1a21540cae32dd64ae6b3bc814b66ce5ed6843e65d112e391>', '<Transaction #1193046/0>']",
            "<Account 0x6b3b2c3f961b2c3f2593338858ca89fa4c0ca247>: ['<Receipt #0x02aea44c3af5b6398a27cf596abadae20a8e61ea37978d6b1bb0d6dec089a674>', '<Transaction #1193046/2>']",
            "<Account 0xa5ed89106ad81162f185e13b624838c693305a78>: ['<Receipt #0x31c027886e28938ab21b8e371f3d3b3f3ff221b2786150b7e91d2bbdd69c4943>', '<Transaction #1193046/1>']",
            "<Account 0xdbcbd5fc3693a8d6262b21376913c655d6e53c99>: ['<Receipt #0xcb13faa6174ee9c1a21540cae32dd64ae6b3bc814b66ce5ed6843e65d112e391>', '<Transaction #1193046/0>']",
            "<Account 0xfbb1b73c4f0bda4f67dca266ce6ef42f520fbb98>: ['<Receipt #0x02aea44c3af5b6398a27cf596abadae20a8e61ea37978d6b1bb0d6dec089a674>', '<Transaction #1193046/2>']"]

        self.maxDiff = None
        self.assertListEqual(accountStrs, expectedAccountStr)

    def test_blockTransactionReceipt_navigation(self):
        # via loader
        receipts_via_loader = [self.loader.get_transaction_receipt(trans.hash) for trans in self.block.transactions]

        # from transaction
        receipts_direct = [trans.get_receipt(self.loader) for trans in self.block.transactions]

        self.assertListEqual(receipts_via_loader, receipts_direct)

        # receipt to transaction
        transacts_from_receipts = [receipt.get_transaction(self.loader) for receipt in receipts_direct]

        self.assertListEqual(transacts_from_receipts, self.block.transactions)