#!/usr/bin/env python3
""" functions"""
from typing import Callable, Iterator, Union, Optional, Tuple, List


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Returns a function that multiplies a float by multiplier.
    """
    def f(n: float) -> float:
        """ To multiplies a float by multiplier """
        return float(n * multiplier)

    return f
