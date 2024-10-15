#!/usr/bin/env python3
""" Module to loop python code 10 times """
import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    function to loop code 10 times
    Arg:
        arg:
    Returns:
    """
    for val in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)