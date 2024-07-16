import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = 'https://manhuatop.org/manhua/the-crazy-genius-composer-returns/chapter-1/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using html5lib parser
    soup = BeautifulSoup(response.content, 'html5lib')
    
    # Find all <div> elements with class 'page-break no-gaps'
    divs = soup.find_all('div', class_='page-break no-gaps')
    
    # List to store all data-src values
    data_src_values = []
    
    # Loop through each <div> and extract data-src values
    for div in divs:
        img_tag = div.find('img', {'data-src': True})
        if img_tag:
            data_src_values.append(img_tag['data-src'])
    
    # Output the data-src values as JSON
    print(json.dumps(data_src_values, indent=2))
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
