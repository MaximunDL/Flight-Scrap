import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener las variables de entorno
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")

# Construir la URI de conexión
uri = f"mongodb+srv://{username}:{password}@scrapdb.lw4npwl.mongodb.net/?retryWrites=true&w=majority&appName=ScrapDB"

try:
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)