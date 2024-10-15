#!/usr/bin/env python3
"""module that Generate list from an async"""
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Func that Collects async generated list and return it"""
    return [_ async for _ in async_generator()]