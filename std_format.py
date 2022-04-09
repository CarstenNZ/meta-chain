import re
from typing import Any

from eth_utils import is_checksum_address, to_checksum_address


class Hex:
    Hex_regex = re.compile('0[xX]([0-9a-fA-F]*)')

    @staticmethod
    def is_hex_addr(address: str) -> bool:
        """ checks if the given string of text type is a valid checksum eth address in
            hexadecimal encoded form
        """
        return is_checksum_address(address)

    @staticmethod
    def to_hex_addr(address: str):
        """ convert to checksum eth address """
        return to_checksum_address(address)

    @staticmethod
    def is_hex(hex_str: Any) -> bool:
        """ checks for any hex string
            - '0x' is a valid hex string
        """
        return isinstance(hex_str, str) and Hex.Hex_regex.fullmatch(hex_str) is not None

    @staticmethod
    def hex_to_int(hex_str: str) -> int:
        assert Hex.is_hex(hex_str)
        return int(hex_str, 16)

    @staticmethod
    def fmt(hex_str: str):
        """ returns hex_str in our standard non-address format (leading 0x, lowercase)
            - throws for invalid hex strings
        """
        assert not Hex.is_hex_addr(hex_str), f"{hex_str} looks like an address, fmt() destroys checksum"

        match = Hex.Hex_regex.fullmatch(hex_str)
        if not match:
            Exception(f"invalid hex string {hex_str}")

        return '0x' + match.group(1).lower()

