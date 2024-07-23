# importing files
import main_page_scrapper
import appending_data_file
# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


import asyncio
import aiohttp



# for demo purpose
# page_url = "https://manhuatop.org/manhua/page/3/?m_orderby=new-manga"
# main_page_scrapper.page_scrap(page_url,headers)


# for scrapping whole website


async def main():
    i=1
    while True:
        page_url = "https://manhuatop.org/manhua/page/"+str(i)+"/?m_orderby=new-manga"
        await main_page_scrapper.page_scrap(page_url,headers=headers)
        print(i)
        i=i+1

if __name__ == "__main__":
    asyncio.run(main())





