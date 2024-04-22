import requests, json, uuid, time, random, os
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson import ObjectId

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno para la conexion a mongoDB
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")

# Construir la URI de conexión
uri = f"mongodb+srv://{username}:{password}@scrapdb.lw4npwl.mongodb.net/?retryWrites=true&w=majority&appName=ScrapDB"

#Funcion para serializar ObjectId a str para JSON
def default_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type not serializable")

def scrape_web(url):
    #Inicializar Listas para almacenar los enlaces y resultados
    product_link = []
    results = []
    #Hacer una peticion GET a la url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Encontras todos los elemntos con beautifulsoap que contienen enlaces de productos
    items = soup.find_all('div', class_='ui-search-item__group ui-search-item__group--title')
    
    #Iterar sobre cada elemento para obtener los enlaces de los productos
    for item in items:
        id = uuid.uuid4()
        link_element = item.find('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link') #
        
        #Verificar si se encontro un enlace y agregarlo a la lista 
        if link_element:
            link = link_element.get('href')
            data = {
                "id": str(id),
                "url": link
            }
            product_link.append(data)

    # Conectar a MongoDB
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['web_scraping']
    collection = db['data']

    #Iterar sobre cada enlace de producto para obtener mas detalles acerca de cada producto
    for link in product_link:
        response = requests.get(link["url"])
        soup = BeautifulSoup(response.text, 'html.parser')  
        
        #Extraer el titulo, el precio y los datos extructurales(datalayer)
        title = soup.find('h1', class_='ui-pdp-title').text.strip()
        price = soup.find('span', class_='andes-money-amount__fraction').text.strip()
        datalayer = soup.find('script', {'type': 'application/ld+json'})
        datalayer_content = json.loads(datalayer.string) if datalayer else None

        #Construir el objeto con la informacion recopilada
        data = {
                "id": str(link["id"]),
                "url": link["url"],
                "tittle": title,
                "precio": price,
                "datalayer": datalayer_content
            }

        # Guardar datos en MongoDB
        collection.insert_one(data)

        #Agregar el objeto a la lista results
        results.append(data)
    return results

#url de la pagina web para hacer scraping
url = 'https://listado.mercadolibre.com.pe/samsung-a32#D[A:samsung%20a32]'
scraped_data = scrape_web(url)

#Nombre del archivo JSON para guardar los datos 
file_name = os.path.join(str(uuid.uuid4()) + ".json")

#Guardar los datos en un archivo JSON
with open(file_name, 'w') as file:
    json.dump(scraped_data, file, indent=4, default=default_serializer)

print("Data scraped and saved to", file_name)