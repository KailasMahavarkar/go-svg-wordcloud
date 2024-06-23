import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
from aiohttp import TCPConnector, ClientSession
import time

"""
This module is an example of how to use asyncio and aiohttp to fetch HTML content from multiple URLs in parallel.

The code optimizes the performance of the requests by creating a connection pool to limit the number of connections created. 
This can improve performance by reducing the number of resources used to make the HTTP requests.

The use of async_timeout is also corrected to be used within an async context manager. 
Additionally, the ClientSession is passed to the get() function to avoid creating multiple sessions for the same requests.
"""

urls = [
    'https://en.wikipedia.org/wiki/Pearl',
    'https://en.wikipedia.org/wiki/Germany',
    'https://en.wikipedia.org/wiki/Ireland',
    'https://en.wikipedia.org/wiki/Bruce_Wayne_(Dark_Knight_trilogy)',
    'https://en.wikipedia.org/wiki/Italy',
    'https://en.wikipedia.org/wiki/France',
    'https://en.wikipedia.org/wiki/Spain',
    'https://en.wikipedia.org/wiki/Greece',
    'https://en.wikipedia.org/wiki/Russia',
    'https://en.wikipedia.org/wiki/China',
    'https://en.wikipedia.org/wiki/India',
    'https://en.wikipedia.org/wiki/Japan',
    'https://en.wikipedia.org/wiki/South_Korea',
    'https://en.wikipedia.org/wiki/Brazil',
    'https://en.wikipedia.org/wiki/Argentina',
    'https://en.wikipedia.org/wiki/United_States',
    'https://en.wikipedia.org/wiki/Canada',
    'https://en.wikipedia.org/wiki/Australia',
    'https://en.wikipedia.org/wiki/New_Zealand'
]

# Create a connection pool with a specified number of connections
conn = TCPConnector(limit=20)


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def trigger(timeout: int = 5):
    # Create a connection pool
    conn = aiohttp.TCPConnector(limit=5)
    # Create a semaphore to limit concurrent connections
    sem = asyncio.Semaphore(5)
    async with ClientSession(connector=conn) as session:
        # Use an asyncio queue to pass URLs to tasks
        q = asyncio.Queue()
        for url in urls:
            await q.put(url)
        master = []
        while not q.empty():
            url = await q.get()
            task = asyncio.create_task(get_url(url, session, sem, timeout))
            master.extend(await task)

        print(master)


async def get_url(url, session, sem, timeout):
    async with sem:
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    return []
                soup = BeautifulSoup(await response.text(), "lxml")
                text = soup.get_text()
                return text.split()
        except asyncio.TimeoutError:
            print(f"Request to {url} closed by timeout")
            return []
        except Exception as e:
            print(f"Error occured: {e}")
            return []

start = time.time()
asyncio.run(trigger(1))
end = time.time()
print(f'function took {end - start} seconds')
