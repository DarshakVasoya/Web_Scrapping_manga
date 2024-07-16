import requests
from bs4 import BeautifulSoup
import json
import codecs
# URL to scrape the list of items
import re


page_url = "https://manhuatop.org/manhua/page/2/?m_orderby=new-manga"


# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# conver views into number
def convert_suffix_to_number(suffix_string):
    suffix_string = suffix_string.lower()
    multipliers = {'k': 1000, 'm': 1000000}

    if suffix_string[-1] in multipliers:
        multiplier = multipliers[suffix_string[-1]]
        return int(float(suffix_string[:-1]) * multiplier)
    else:
        return int(float(suffix_string))
# Function to extract details from each item's page
def extract_details(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        
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
        status= soup.find('div', class_='post-status').find('div', class_='summary-content').find_next('div', class_='summary-content').text.strip()

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
            'Total views':convert_suffix_to_number(total_view)
        }
    else:
        print(f"Failed to retrieve the detailed page. Status code: {response.status_code}")
        return None

# Function to fetch data-src values from chapter pages
def fetch_data_src_values(base_url):
    chapter = 1
    all_data_src_values = {}

    while True:
        url = f'{base_url}chapter-{chapter}/'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')
            divs = soup.find_all('div', class_='page-break no-gaps')
            
            if not divs:
                break  # No more chapters with 'page-break no-gaps'
            
            data_src_values = []
            for div in divs:
                img_tag = div.find('img', {'data-src': True})
                if img_tag:
                    data_src_values.append(img_tag['data-src'])
            
            all_data_src_values[f'chapter-{chapter}'] = data_src_values
            chapter += 1
        else:
            print(f'Failed to retrieve chapter {chapter}. Status code: {response.status_code}')
            break

    return all_data_src_values




# page scraping

def page_scrap(list_url):
    
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
                details = extract_details(href) if href else {}
                
                # Fetch chapter data-src values
                chapter_data_src = fetch_data_src_values(href) if href else {}
                
                # Append the extracted data to the list
                data.append({
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

        
        # Print the extracted data in JSON format
        # print(json.dumps(data, indent=4)) //to print json data
        file_path = "data.json"

        # Open the file in write mode
        with open(file_path, 'a') as json_file:
            # Write the dictionary data into the file
            json.dump(data, json_file, indent=4)
        
        file_path = "dataError.json"

        # Open the file in write mode
        with open(file_path, 'a') as json_file:
            # Write the dictionary data into the file
            json.dump(error_link, json_file, indent=4)

    else:
        print(f"Failed to retrieve the list page. Status code: {response.status_code}")


list_url = 'https://example.com/list'

page_scrap(page_url)
# i=1
# while True:
#     page_url = "https://manhuatop.org/manhua/page/"+str(i)+"/?m_orderby=new-manga"
#     page_scrap(page_url)
#     print(i)
#     i=i+1


hrllock to check gitgit 