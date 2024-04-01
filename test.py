import requests, json, uuid, time, random
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

def scrape_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    variables_html = [item.text.strip() for item in soup.find_all('div', {'class': 'ui-search-item__group'})]
    precios = [item.text.strip() for item in soup.find_all('div', {'class': 'ui-search-price__second-line'})]

    datalayer_script = soup.find('script', {'id': 'datalayer'})
    datalayer = datalayer_script.text if datalayer_script else None

    file_name = str(uuid.uuid4()) + ".json"

    data = {
        "variables_html": variables_html,
        "precios": precios,
        "datalayer": datalayer,
        "time": datetime.now().isoformat()
    }

    with open(file_name, 'w') as file:
        json.dump(data, file)

    return data, file_name
  

url = 'https://listado.mercadolibre.com.pe/samsung-a32#D[A:samsung%20a32]'

scrape_data, file_name = scrape_web(url)

time.sleep(random.uniform(3, 5))