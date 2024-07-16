import Convertors_to_number as convert
import requests
from bs4 import BeautifulSoup


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
            'Total views':convert.convert_suffix_to_number(total_view)
        }
    else:
        print(f"Failed to retrieve the detailed page. Status code: {response.status_code}")
        return None
