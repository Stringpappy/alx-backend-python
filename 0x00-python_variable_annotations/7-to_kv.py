#!/usr/bin/env python3
""" string and int/float to tuple"""
from typing import Callable, Iterator, Union, Optional, Tuple, List


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    To take iny and float as parameter and return string and float
    """

    return (k, v**2)
