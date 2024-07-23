import requests
from bs4 import BeautifulSoup
import json
import aiohttp
# importing files
import Convertors_to_number as convertor
import second_sepcial_each_manga as Extractor_specialPage
import extractor_chaptor
import appending_data_file as append_data
import sys
import aiofiles
# page scraping

async def page_scrap(list_url,headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(list_url, headers=headers) as response:
            # Send a GET request to the list URL
            # Check if the request was successful
            if response.status == 200:
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(await response.text(), 'html5lib')
                
                # Find all items with the specified class
                items = soup.find_all('div', class_='col-12 col-md-6 badge-pos-1')
                error_link = {}
                
                # Loop through the found items and extract the desired data
                for item in items:
                    try:
                        # Extract href and title
                        link = item.find('a')
                        href = link['href'] if link else None
                        title = link['title'] if link else None
                        
                        # Extract img
                        img = item.find('img')
                        img_src = img['data-src'] if img else None
                        
                        # Extract rating
                        try:
                            rating = item.find('span', class_='score font-meta total_votes')
                            rating_text = rating.text.strip() if rating else None
                        except:
                            rating_text=None    
                    
                        # Extract date
                        try:
                            date = item.find('span', class_='post-on font-meta')
                            date_text = date.text.strip() if date else None
                        except:
                            date_text=None

                        # Extract last chapter
                        try:
                            chapter = item.find('a', class_='btn-link')
                            chapter_text = chapter.text.strip() if chapter else None
                        except:
                            chapter_text=None
                        # Extract detailed information from the item's page
                        details =   await Extractor_specialPage.extract_details(href,headers=headers) if href else {}
                        
                        # Fetch chapter data-src values
                        chapter_data_src = await  extractor_chaptor.fetch_data_src_values(href,headers=headers,total_chapter_list= details['Total_chapter_list'] ) if href else {}
            
                        file_path = "data.json"
                        # Append the extracted data to the list
                        if details.get('Total_chapter_list'):
                            await append_data.append_to_mongodb( {
                                'href': href,
                                'title': title,
                                'cover_img': img_src,
                                'rating': rating_text,
                                'chapter': chapter_text,
                                'date': date_text,
                                'image_url': details.get('image_url'),
                                'genres': details.get('genres'),
                                'summary': details.get('summary'),
                                'release_year': details.get('release_year'),
                                'alternative': details.get('alternative'),
                                'status': details.get('status'),
                                'Total views':details.get('Total views'),
                                'Total chapters':details.get('Total_chapter_list'),
                                'chapters': chapter_data_src
                            })
                    except Exception as e:
                        # error_link[title]=href
                    
                        await append_data.append_to_mongodb_error({title:href})
                        print(f"Error processing item 8: {e}")

            #    notie that here dataError store dictionary , while data.json file store list. so , we can not use same function
                
            

            else:
                print(f"Failed to retrieve the list page. Status code: {response.status}")
                
                async with aiofiles.open("page_error.json", 'w') as file:
                    await file.write(json.dumps({1:list_url}, indent=4))
                sys.exit()

