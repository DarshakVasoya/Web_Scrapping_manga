import Convertors_to_number as convert
import requests
from bs4 import BeautifulSoup
import re
import aiohttp
def total_chaptors(soup):
    lis = soup.find('ul', class_='main version-chap no-volumn').find_all('li')
    total_chaptor_list=[]
    for li in lis:
        total_chaptor_list.append(li.find('a').text.strip())
    return total_chaptor_list




# Function to extract details from each item's page
async def extract_details(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html5lib')
                total_chapter_list= total_chaptors(soup)
                # Extract image URL
                image_div = soup.find('div', class_='tab-summary').find('div', class_='summary_image')
                image_url = image_div.find('img')['data-src'] if image_div else None

                # Extract genres
                try:
                    genres_div = soup.find('div', class_='tcc_wrap').find('div', class_='genres-content')
                    genres = [genre.text for genre in genres_div.find_all('a')] if genres_div else None
                except:
                    genres=[]
                # Extract total views
                try:
                    total_view=soup.find('div', class_='post-content_item').find_next('div', class_='post-content_item').find('div', class_='summary-content').text.strip()
                    total_view=re.search(r'\d+\.\d+K', total_view).group()
                except: 
                    total_view="0"  

                # Extract alternative titles
                try:
                    post_content_items = soup.find_all('div', class_='post-content_item')
                    alternative_text = None
                    for item in post_content_items:
                        heading = item.find('div', class_='summary-heading')
                        if heading and "Alternative" in heading.text:
                            content = item.find('div', class_='summary-content')
                            alternative_text = content.text.strip() if content else None
                            break
                except:
                    alternative_text = None

                # Extract summary
                try:    
                    summary_div = soup.find('div', class_='c-page-content style-1').find('div', class_='summary__content')
                    summary = summary_div.find('p').text if summary_div else None
                except:
                    summary=""
                
                # Extract status
                
                try:
                    status= soup.find('div', class_='post-status').find('div', class_='summary-content').find_next('div', class_='summary-content').text.strip()
                except:
                    status="OnGoing"

                try:
                    # Extract release year
                    release_div = soup.find('div', class_='post-status').find('div', class_='summary-content')
                    release_year = release_div.find('a').text if release_div else None
                except:
                    release_year=None


                return {
                    'image_url': image_url,
                    'genres': genres,
                    'summary': summary,
                    'release_year': release_year,
                    'alternative': alternative_text,
                    'status':status,
                    'Total views':convert.convert_suffix_to_number(total_view),
                    'Total_chapter_list': total_chapter_list
                }
            else:
                print(f"Failed to retrieve the detailed page. Status code: {response.status}")
                return None
