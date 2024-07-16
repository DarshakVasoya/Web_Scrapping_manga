

import requests
from bs4 import BeautifulSoup
import json

# URL to scrape the list of items
list_url = "https://manhuatop.org/manhua/page/2/?m_orderby=new-manga"

# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to extract details from each item's page
def extract_details(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        
        # Extract image URL
        image_div = soup.find('div', class_='tab-summary').find('div', class_='summary_image')
        image_url = image_div.find('img')['data-src'] if image_div else None

        # Extract genres
        genres_div = soup.find('div', class_='tcc_wrap').find('div', class_='genres-content')
        genres = [genre.text for genre in genres_div.find_all('a')] if genres_div else None

        # Extract summary
        summary_div = soup.find('div', class_='c-page-content style-1').find('div', class_='summary__content')
        summary = summary_div.find('p').text if summary_div else None

        # Extract release year
        release_div = soup.find('div', class_='post-status').find('div', class_='summary-content')
        release_year = release_div.find('a').text if release_div else None

        return {
            'image_url': image_url,
            'genres': genres,
            'summary': summary,
            'release_year': release_year
        }
    else:
        print(f"Failed to retrieve the detailed page. Status code: {response.status_code}")
        return None

# Send a GET request to the list URL
response = requests.get(list_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html5lib')
    
    # Find all items with the specified class
    items = soup.find_all('div', class_='col-12 col-md-6 badge-pos-1')
    
    data = []
    
    # Loop through the found items and extract the desired data
    for item in items:
        # Extract href and title
        link = item.find('a')
        href = link['href'] if link else None
        title = link['title'] if link else None
        
        # Extract img
        img = item.find('img')
        img_src = img['data-src'] if img else None

        # Extract rating
        rating = item.find('span', class_='score font-meta total_votes')
        rating_text = rating.text.strip() if rating else None
        
        # Extract 
        date = item.find('span', class_='post-on font-meta')
        date_text = date.text.strip() if date else None

        # Extract last chapter
        chapter = item.find('a', class_='btn-link')
        chapter_text = chapter.text.strip() if chapter else None
        
        # Extract detailed information from the item's page
        details = extract_details(href) if href else {}
        
        # Append the extracted data to the list
        data.append({
            'href': href,
            'title': title,
            'img': img_src,
            'rating': rating_text,
            'chapter': chapter_text,
            'date': date_text,
            'image_url': details.get('image_url'),
            'genres': details.get('genres'),
            'summary': details.get('summary'),
            'release_year': details.get('release_year')
        })
    
    # Print the extracted data in JSON format
    print(json.dumps(data, indent=4))
else:
    print(f"Failed to retrieve the list page. Status code: {response.status_code}")

