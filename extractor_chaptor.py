import requests
from bs4 import BeautifulSoup

import aiohttp
import asyncio

async def fetch_data_src_values(base_url, headers, total_chapter_list):
    all_data_src_values = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        
        for chapter in reversed(total_chapter_list):
            url = f'{base_url}{chapter.lower().replace(" ","-")}/'
            tasks.append(fetch_chapter_data(session, url, chapter, all_data_src_values))

        await asyncio.gather(*tasks)

    return all_data_src_values


async def fetch_chapter_data(session, url, chapter, all_data_src_values):
    async with session.get(url) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'html5lib')
            divs = soup.find_all('div', class_='page-break no-gaps')
            data_src_values = []
            for div in divs:
                img_tag = div.find('img', {'data-src': True})
                if img_tag:
                    data_src_values.append(img_tag['data-src'])
            if data_src_values:
                all_data_src_values[chapter] = data_src_values
        else:
            print(f'Failed to retrieve chapter {chapter}. Status code: {response.status}')
