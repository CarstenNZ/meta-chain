import json
import sqlite3
import zlib
from pathlib import Path
from typing import Optional

from cache.base import Cache
from chainmodel.base_model import Block, Receipt, Contract, Code, Trace
from config import Config


class Sqlite:
    """ simple key:value database
    """
    def __init__(self, db_path: Path):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS key_value (key STRING PRIMARY KEY ASC, value STRING, compress BOOL);")
        self.con.commit()

    def add(self, key: str, value: str):
        if not isinstance(value, str):
            raise Exception("accepts str only")

        if compress := len(value) > 1024:
            value = zlib.compress(value.encode(), 3)

        self.cur.execute("REPLACE INTO key_value (key,value,compress) values(?,?,?)", (key, value, compress))
        self.con.commit()

    def get(self, key: str) -> Optional[str]:
        res = self.cur.execute("SELECT value, compress FROM key_value WHERE key IS ?", (key,)).fetchone()
        if res is None:
            return None

        value, compress = res
        return zlib.decompress(value).decode() if compress else value

    def close(self):
        self.con.commit()
        self.con.close()
        self.con = self.cur = None


# noinspection PyUnresolvedReferences
class DBCache(Cache):
    _Block_Prefix = 'b'
    _Receipt_Prefix = 'r'
    _Code_Prefix = 'c'
    _Trace_Prefix = 't'

    def __init__(self, config: Optional[Config], clear=False, explicit_path=None):
        """
            - explicit_path overrides config (config can be Null in this case)
            - clear creates an empty cache
        """

        file_path = explicit_path or config.get_cache_path()
        if clear:
            Path(file_path).unlink(missing_ok=True)

        self._db = Sqlite(file_path)

    def add_block(self, block: Block, block_dict: dict):
        self._db.add(f'{self._Block_Prefix}{block.number}', json.dumps(block_dict))

    def get_block(self, block_cls, block_number: int):
        block_src = self._db.get(f'{self._Block_Prefix}{block_number}')
        if block_src is None:
            return None, None

        # noinspection PyTypeChecker
        block_src = json.loads(block_src)
        return block_cls(block_src), block_src

    def add_transaction_receipt(self, receipt: Receipt, receipt_dict: dict):
        self._db.add(self._Receipt_Prefix + receipt.transactionHash, json.dumps(receipt_dict))

    def get_transaction_receipt(self, receipt_cls, transaction_hash):
        receipt_src = self._db.get(self._Receipt_Prefix + transaction_hash)
        if receipt_src is None:
            return None, None

        # noinspection PyTypeChecker
        receipt_src = json.loads(receipt_src)
        return receipt_cls(receipt_src), receipt_src

    def add_code(self, code: Contract, code_bytes: str):
        self._db.add(self._Code_Prefix + code.address, code_bytes)

    def get_code(self, code_cls, contract_address):
        contract_src = self._db.get(self._Code_Prefix + contract_address)
        if contract_src is None:
            return None, None

        return Code(contract_address, contract_src), contract_src

    def add_transaction_trace(self, trace: Trace, trace_dict: dict):
        self._db.add(self._Trace_Prefix + trace.address, json.dumps(trace_dict))

    def get_transaction_trace(self, trace_cls, transaction_address):
        trace_src = self._db.get(self._Trace_Prefix + transaction_address)
        if trace_src is None:
            return None, None

        return trace_cls(transaction_address, json.loads(trace_src)), trace_src

    def close(self):
        if self._db:
            self._db.close()
            self._db = None

    def __enter__(self):
        assert self._db is not None
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.close()

    def __del__(self):
        self.close()
