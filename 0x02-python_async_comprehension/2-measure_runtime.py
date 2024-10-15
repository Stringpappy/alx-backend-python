#!/usr/bin/env python3
""" module that measure the execution time"""
import time
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    function that execute async_com 4 times
    """
    time_to_start = time.perf_counter()
    task = [async_comprehension() for i in range(4)]
    await asyncio.gather(*task)
    time_to_end = time.perf_counter()
    return (time_to_end - time_to_start)