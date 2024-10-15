import asyncio
import random

async def wait_random(max_delay=10):
    """generte random number from 1 to max delay """
    random_delay = random.uniform(0, max_delay) 
    """
    uniform generate a random floating number
    asynchronusly wait for the generated delay random_delay"""
    await asyncio.sleep(random_delay)

    return random_delay

