import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}



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

