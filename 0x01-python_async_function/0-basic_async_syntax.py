import asyncio
from random import randint

# Assume wait_random is defined as follows
async def wait_random(max_delay: int) -> list[float]:
    delay = randint(0, max_delay)
    await asyncio.sleep(delay)
    return delay

def task_wait_random(max_delay: int) -> asyncio.Task:
    return asyncio.create_task(wait_random(max_delay))


wait_random = __import__('0-basic_async_syntax').wait_random

print(asyncio.run(wait_random(0)))
print(asyncio.run(wait_random(5)))
print(asyncio.run(wait_random(15)))

