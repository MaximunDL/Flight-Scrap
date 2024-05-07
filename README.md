## Scraper de Productos

Este es un script Python diseñado para extraer información de productos desde diversas páginas web de comercio electrónico. Utiliza técnicas de web scraping para obtener detalles como el título, el precio y datos estructurados de productos a partir de URLs específicas proporcionadas en una hoja de cálculo de Google Sheets.

## Uso
1. Configuración de la Hoja de Cálculo de Google Sheets:
- Cree una hoja de cálculo en Google Sheets con dos columnas: una para las URLs de los productos y otra para el estado (activo o inactivo) de cada URL.
- Asegúrese de que la hoja de cálculo tenga permisos de lectura para el servicio de Google Sheets.

2. Configuración de Variables de Entorno:
- Cree un archivo .env en el directorio raíz del proyecto y defina las siguientes variables de entorno:

#### .env.example

```http
  MONGODB_USERNAME=your_username
  MONGODB_PASSWORD=your_password
  MONGODB_NAME=your_database_name
```
3. Instalación de Dependencias:
- Ejecute pip install -r requirements.txt para instalar las dependencias necesarias.

4. Ejecución del script:
- Ejecute el script Python "scraping-web.py" para iniciar el proceso de scraping.
- El script recuperará las URLs activas de la hoja de cálculo de Google Sheets y luego extraerá información detallada de cada producto de las páginas web correspondientes.
- Los datos recopilados se almacenarán en una base de datos MongoDB.


## Requisitos Previos

- Python 3.x
- Cuenta de Google con acceso a Google Sheets API y Google Drive API
- Una Instancia de MongoDB

## Notas

- Asegúrese de que las URLs proporcionadas en la hoja de cálculo sean accesibles públicamente y que los productos estén disponibles para su visualización sin necesidad de autenticación.
- Este script está diseñado para usos educativos o de investigación. Asegúrese de cumplir con los términos de servicio de cualquier sitio web que esté scrapeando.
