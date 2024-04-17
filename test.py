import requests, json, uuid, time, random
from bs4 import BeautifulSoup
from datetime import datetime
#import mongoinit

def scrape_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('div', class_='ui-search-item__group ui-search-item__group--title')
    data_list = []

    for item in items:
        link_element = item.find('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')
        variables_html = [item.text.strip() for item in soup.find_all('div', {'class': 'ui-search-item__group'})]
        precios = [item.text.strip() for item in soup.find_all('div', {'class': 'ui-search-price__second-line'})]

        if link_element:
            link = link_element.get('href')
            data = {
                "link": link,
                "time": datetime.now().isoformat(),
                "variables": variables_html,
                "precios": precios
            }
            data_list.append(data)

    return data_list

url = 'https://listado.mercadolibre.com.pe/samsung-a32#D[A:samsung%20a32]'
scraped_data = scrape_web(url)

file_name = str(uuid.uuid4()) + ".json"

with open(file_name, 'w') as file:
    json.dump(scraped_data, file, indent=4)

print("Data scraped and saved to", file_name)