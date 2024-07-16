import requests
from bs4 import BeautifulSoup
import json



# URL to scrape
url = "https://manhuatop.org/manhua/page/2/?m_orderby=new-manga"

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
        
        # Extract date
        date = item.find('span', class_='post-on font-meta')
        date_text = date.text.strip() if date else None

        # last cheptor
        chapter = item.find('a', class_='btn-link')
        chapter_text = chapter.text.strip() if chapter else None


        
        
        # Append the extracted data to the list
        data.append({
            'href': href,
            'title': title,
            'img': img_src,
            'rating': rating_text,
            'chapter':chapter_text,
            'date': date_text
        })


    
    # Print the extracted data in JSON format
    print(json.dumps(data, indent=4))


    # print(len(json.dumps(data, indent=4)))
    

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")



