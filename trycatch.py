import requests
from bs4 import BeautifulSoup
import json

# URL to scrape the list of items
list_url = "https://manhuatop.org/manhua/page/1/?m_orderby=new-manga"

# Headers to include in the request to avoid 403 errors
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to extract details from each item's page
def extract_details(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        soup = BeautifulSoup(response.content, 'html5lib')
        
        # Extract image URL
        image_div = soup.find('div', class_='tab-summary').find('div', class_='summary_image')
        image_url = image_div.find('img')['data-src'] if image_div else None

        # Extract genres
        genres_div = soup.find('div', class_='tcc_wrap').find('div', class_='genres-content')
        genres = [genre.text for genre in genres_div.find_all('a')] if genres_div else None
        
        # Extract alternative titles
        post_content_items = soup.find_all('div', class_='post-content_item')
        alternative_text = None
        for item in post_content_items:
            heading = item.find('div', class_='summary-heading')
            if heading and "Alternative" in heading.text:
                content = item.find('div', class_='summary-content')
                alternative_text = content.text.strip().split('/') if content else None
                break
    
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
            'release_year': release_year,
            'alternative': alternative_text
        }
    except Exception as e:
        print(f"Failed to extract details from {url}: {e}")
        return None

# Function to fetch data-src values from chapter pages
def fetch_data_src_values(base_url):
    try:
        chapter = 1
        all_data_src_values = {}

        while True:
            url = f'{base_url}chapter-{chapter}/'
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            
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

        return all_data_src_values
    except Exception as e:
        print(f"Failed to fetch data-src values from {base_url}: {e}")
        return {}

# Send a GET request to the list URL
try:
    response = requests.get(list_url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html5lib')
    
    # Find all items with the specified class
    items = soup.find_all('div', class_='col-12 col-md-6 badge-pos-1')
    
    data = []
    
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
            rating = item.find('span', class_='score font-meta total_votes')
            rating_text = rating.text.strip() if rating else None
            
            # Extract date
            date = item.find('span', class_='post-on font-meta')
            date_text = date.text.strip() if date else None

            # Extract last chapter
            chapter = item.find('a', class_='btn-link')
            chapter_text = chapter.text.strip() if chapter else None
            
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
                'chapters': chapter_data_src
            })
        except Exception as e:
            print(f"Failed to extract data from item: {e}")
            if href:
                print("error")
                # data.append({'href': href, 'error': str(e)})
    
    # Print the extracted data in JSON format
    print(json.dumps(data, indent=4))

except Exception as e:
    print(f"Failed to retrieve the list page: {e}")
