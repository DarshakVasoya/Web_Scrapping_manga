import requests
from bs4 import BeautifulSoup
import json

# importing files
import Convertors_to_number as convertor
import second_sepcial_each_manga as Extractor_specialPage
import extractor_chaptor
import appending_data_file as append_data

# page scraping

def page_scrap(list_url,headers):
    
    # Send a GET request to the list URL
    response = requests.get(list_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html5lib')
        
        # Find all items with the specified class
        items = soup.find_all('div', class_='col-12 col-md-6 badge-pos-1')
        
        data = []
        error_link={}
        
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
                details =  Extractor_specialPage.extract_details(href,headers=headers) if href else {}
                
                # Fetch chapter data-src values
                chapter_data_src = extractor_chaptor.fetch_data_src_values(href,headers=headers ) if href else {}
                
                file_path = "data.json"
                # Append the extracted data to the list
                append_data.append_to_json_file(file_path, {
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
                    'chapters': chapter_data_src
                })
            except Exception as e:
                error_link[title]=href
                print(f"Error processing item: {e}")

       
        file_path = "dataError.json"
        append_data.append_to_json_file(file_path,error_link)
        

    else:
        print(f"Failed to retrieve the list page. Status code: {response.status_code}")
