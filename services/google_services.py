import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

def get_urls_from_google_sheet():
    # Configurar el sistema de registro
    logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
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