import requests
from bs4 import BeautifulSoup
import json
import codecs
# URL to scrape the list of items
import re

# importing files
import Convertors_to_number as convertor
import second_sepcial_each_manga as Extractor_specialPage
import extractor_chaptor
import main_page_scrapper

page_url = "https://manhuatop.org/manhua/page/2/?m_orderby=new-manga"


# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

main_page_scrapper.page_scrap(page_url,headers)


# i=1
# while True:
#     page_url = "https://manhuatop.org/manhua/page/"+str(i)+"/?m_orderby=new-manga"
#     page_scrap(page_url)
#     print(i)
#     i=i+1