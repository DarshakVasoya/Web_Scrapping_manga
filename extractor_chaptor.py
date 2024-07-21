import requests
from bs4 import BeautifulSoup




# Function to fetch data-src values from chapter pages

# Function to fetch data-src values from chapter pages
def fetch_data_src_values(base_url, headers,total_chapter_list):
   
    all_data_src_values = {}
   
    for chapter in reversed(total_chapter_list):
        url = f'{base_url}{chapter.lower().replace(" ","-")}/'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html5lib')
            divs = soup.find_all('div', class_='page-break no-gaps')
            data_src_values = []
            for div in divs:
                img_tag = div.find('img', {'data-src': True})
                if img_tag:
                    data_src_values.append(img_tag['data-src'])
            if data_src_values:
                all_data_src_values[chapter] = data_src_values
            
        else:
            print(f'Failed to retrieve chapter {chapter}. Status code: {response.status_code}')
            continue
        

    return all_data_src_values
