from typing import Union, Sequence, Set, ValuesView, Generator


def first(seq: Union[Sequence, Set, ValuesView, Generator]):
    """ return first element in seq, will throw on empty seq
        - faster than next(iter(seq)) according to https://stackoverflow.com/a/48874729
        - especially good for non-index able sequences like sets
    """
    for r in seq:
        return r
