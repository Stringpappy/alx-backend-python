#!/usr/bin/env python3
""" duck type an iterable object"""
from typing import Mapping, MutableMapping, Sequence, Iterable, Tuple, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Return Element length """
    return [(i, len(i)) for i in lst]
