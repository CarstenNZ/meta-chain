import re


class Hex:
    Hex_regex = re.compile('(?:0[xX])([0-9a-fA-F]+)')

    @staticmethod
    def isHexStr(hex_str):
        return Hex.Hex_regex.match(hex_str) is not None

    @staticmethod
    def fmt(hex_str):
        """ returns hex_str in our standard format (leading 0x, lowercase)
            - throws for invalid hex strings
        """
        match = Hex.Hex_regex.match(hex_str)
        if not match:
            Exception(f"invalid hex string {hex_str}")
        return '0x' + match.group(1).lower()

