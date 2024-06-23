import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
import time

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


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def trigger(timeout: int = 5):
    tasks = [asyncio.create_task(get(url=url)) for url in urls]

    try:
        with async_timeout.timeout(timeout):
            await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        return "Request Closed by Timeout: {}"
    finally:
        master = []
        for i, task in enumerate(tasks):
            if task.done() and not task.cancelled():
                soup = BeautifulSoup(task.result(), "lxml")
                for x in str(soup.get_text()).replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').split(' '):
                    master.append(x)
                print(f'Task is finished')
            else:
                print(f"Task hasn't been finished.")

        # print(master)


start = time.time()
asyncio.run(trigger(1))
end = time.time()
print(f'function took {end - start} seconds')
