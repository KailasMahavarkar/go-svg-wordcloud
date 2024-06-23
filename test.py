import aiohttp
import asyncio
from bs4 import BeautifulSoup
from wordfilter import WordFilter

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    return links

async def search_links(url):
    html = await fetch_html(url)
    links = await extract_links(html)
    return links

async def main():
    url = 'https://example.com'
    links = await search_links(url)
    print(links)

if __name__ == '__main__':
    words = asyncio.run(main())
    print(words)


