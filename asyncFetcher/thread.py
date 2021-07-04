import aiohttp
import asyncio
import async_timeout
from bs4 import BeautifulSoup
from svgPro.wordfilter import WordFilter
from time import time_ns

# urls = [
#     'https://en.wikipedia.org/wiki/Pearl',
#     'https://en.wikipedia.org/wiki/Germany',
#     'https://en.wikipedia.org/wiki/Ireland',
#     'https://en.wikipedia.org/wiki/Bruce_Wayne_(Dark_Knight_trilogy)'
# ]

urls = [
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/3',
    'http://httpbin.org/delay/1',
    'http://httpbin.org/delay/1'
]

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main(timeout: float = 5.0):
    tasks = [asyncio.create_task(get(url=url)) for url in urls]
    try:
        with async_timeout.timeout(timeout):
            await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        print('timeout')
    finally:
        master = []
        status = [task.done() and not task.cancelled() for i, task in enumerate(tasks)]
        print(status)
        for i, task in enumerate(tasks):
            if task.done() and not task.cancelled():
                soup = BeautifulSoup(task.result(), "lxml")
                for x in str(soup.get_text()).replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').split(' '):
                    master.append(x)

        print(master)
        print(WordFilter(words=master, stoptypes=['basic', 'max'], minoccurence=1, minlength=1))

start = time_ns()
asyncio.run(main(2))
end = time_ns()


print(f"finished in {(end - start) / (10**9)} seconds")