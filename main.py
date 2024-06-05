import requests, json, uuid, time, random, os, schedule, traceback, logging
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurar el sistema de registro
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno para la conexión a MongoDB
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
db_name = os.getenv("MONGODB_NAME")

# Construir la URI de conexión [string de conexión]
uri = f"mongodb+srv://{username}:{password}@projectpy.sgszczz.mongodb.net/?retryWrites=true&w=majority&appName={db_name}"

# Función para serializar ObjectId a str para JSON
def default_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type no serializable")

def get_urls_from_google_sheet():
    # Loggear la carga de credenciales del servicio de Google Sheets
    logging.info("Cargando credenciales del servicio de Google Sheets...")
    
    # Cargar las credenciales del servicio de Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("./sheets-credential.json", scope)
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo
    sheet = client.open("Links_product").sheet1 # Nombre de la hoja

    # Obtener todos los valores de la columna B (urls) y C (status)
    urls_and_statuses = sheet.get("B1:C")  # asumiendo que las URLs comienzan desde la fila 1 y el estado desde la columna C

    # Filtrar las URLs que tienen status 'True'
    valid_urls = [url for url, status in urls_and_statuses if status.lower() == 'true']

    # Loggear la cantidad de URLs válidas encontradas
    logging.info(f'Se encontraron {len(valid_urls)} URLs válidas en la hoja de cálculo.')

    return valid_urls

def scrape_web(url):
    # Loggear el inicio del scraping para una URL específica
    logging.info(f'Iniciando scraping para la URL: {url}')

    # Conectar a MongoDB
    client = MongoClient(uri)
    db = client['scrapdb']
    collection = db['data']

    # Inicializar Listas para almacenar los enlaces y resultados
    product_link = []
    results = []

    # Hacer una petición GET a la url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos los elementos con beautifulsoup que contienen enlaces de productos
    items = soup.find_all('div', class_='ui-search-item__group ui-search-item__group--title')

    # Iterar sobre cada elemento para obtener los enlaces de los productos
    for item in items:
        id = ObjectId()  # Utilizando ObjectId de pymongo
        link_element = item.find('a', class_='ui-search-item__group__element ui-search-link__title-card ui-search-link')

        # Verificar si se encontró un enlace y agregarlo a la lista
        if link_element:
            link = link_element.get('href')
            data = {
                "id": str(id),
                "url": link
            }
            product_link.append(data)

    # Iterar sobre cada enlace de producto para obtener más detalles acerca de cada producto
    for link in product_link:
        response = requests.get(link["url"])
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer el título, el precio y los datos estructurales (datalayer)
        title = soup.find('h1', class_='ui-pdp-title').text.strip()
        price = soup.find('span', class_='andes-money-amount__fraction').text.strip()
        datalayer = soup.find('script', {'type': 'application/ld+json'})
        datalayer_content = json.loads(datalayer.string) if datalayer else None

        # Construir el objeto con la información recopilada
        data = {
            "id": str(link["id"]),
            "url": link["url"],
            "title": title,
            "precio": price,
            "datalayer": datalayer_content
        }

        # Guardar datos en MongoDB
        collection.insert_one(data)

        # Agregar el objeto a la lista results
        results.append(data)

    # Loggear el fin del scraping para una URL específica
    logging.info(f'Scraping completado para la URL: {url}')

    return results

# Obtener las URLs válidas desde la hoja de cálculo de Google Sheets
valid_urls = get_urls_from_google_sheet()

# Procesar solo las URLs válidas
for url in valid_urls:
    scraped_data = scrape_web(url)

# En este punto, ya has raspado y guardado en MongoDB solo las URLs válidas.
logging.info("Scraping completo y datos guardados en MongoDB.")

# Programación de la tarea de scraping cada vez que especifiquemos el tiempo
schedule.every().hour.do(lambda: [scrape_web(url) for url in valid_urls])

# Bucle para ejecutar la programación de la tarea
while True:
    schedule.run_pending()
    time.sleep(1)
