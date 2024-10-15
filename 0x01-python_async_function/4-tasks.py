#!/usr/bin/env python3
"""
asyncio
"""
import time 
import asyncio
from typing import List

task_wait_random = __import__("3-tasks.py").wait_n 

async def  task_wait_n( int, max_dekay: int) -> list[float]:
    """func that take code  from wait_n and alter into new func"""
    wait_times = asyncio.gather(
        *turple(map(lambda _: task_wait_random(max_delay), range(n)
        ))
    )
    return sorted(wait_times)