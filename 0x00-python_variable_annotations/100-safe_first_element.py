#!/usr/bin/env python3
""" first element of a sequence """
from typing import Any, Union, Sequence, Iterable, List, Tuple


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ To Safe first element """
    if lst:
        return lst[0]
    else:
        return None
