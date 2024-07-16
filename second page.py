

import requests
from bs4 import BeautifulSoup
import re

# URL to scrape
url = "https://manhuatop.org/manhua/the-crazy-genius-composer-returns/"

# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
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

    # Extract status
    status= soup.find('div', class_='post-status').find('div', class_='summary-content').find_next('div', class_='summary-content').text.strip()

    # Extract total views
    total_view=soup.find('div', class_='post-content_item').find_next('div', class_='post-content_item').find('div', class_='summary-content').text.strip()
    total_view=re.search(r'\d+\.\d+K', total_view).group()
    
    
    
    post_content_items = soup.find_all('div', class_='post-content_item')

    alternative_text = None
    for item in post_content_items:
        heading = item.find('div', class_='summary-heading')
        if heading and "Alternative" in heading.text:
            content = item.find('div', class_='summary-content')
            alternative_text = content.text.strip() if content else None
            break

    # Print the extracted information
    print(f"Image URL: {image_url}")
    print(f"Genres: {genres}")
    print(f"Summary: {summary}")
    print(f"Release Year: {release_year}")
    print(f"Status: {status}")
    print(f"Total views: {total_view}")
    
    print(f"Alternative Titles: {alternative_text}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

