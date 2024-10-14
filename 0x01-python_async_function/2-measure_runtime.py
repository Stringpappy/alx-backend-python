import time
import asyncio

wait_n = __import__("1-concurrent_cooroutines").wait_n



def measure_time(n: int, max_dlay: int) -> float:
    start_time = time.time
    asyncio.run(wait_n(n, max_delay))
    return (time.time() - start_time) / n
