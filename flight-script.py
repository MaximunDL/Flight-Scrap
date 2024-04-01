import requests, json, uuid, time, random
from bs4 import BeautifulSoup
from datetime import datetime
# from pymongo import mongo_client
import time 
import random

def scrape_web(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    variables_html = [str(tag) for tag in soup.find_all('div', class_='app-journey-fares-item')]
    precios = [str(tag) for tag in soup.find_all('precios')]

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

url = 'https://flights.pacificcoastal.com/en/'

scraped_data, file_name = scrape_web(url)

print("Datos guardados en archivo Json", file_name)

time.sleep(random.uniform(3, 5))