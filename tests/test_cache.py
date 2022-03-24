import os
import unittest

from cache.shelve import ShelveCache
from tests.test_chainmodel import TestChainModel


class TestShelveCache(unittest.TestCase):
    def test_createShelfCache(self):
        dbPath = '/tmp/test.shelve'
        block = TestChainModel().test_createDataObjectFromDict()

        with ShelveCache(dbPath, clear=True) as db:
            db.add_block(block)

        with ShelveCache(dbPath) as db:
            cache_block = db.get_block(block.number)

        os.remove(dbPath)

        assert block.hash == cache_block.hash

