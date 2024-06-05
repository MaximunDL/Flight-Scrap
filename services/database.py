import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

def connect_to_mongodb():

    # Cargar variables de entorno desde .env
    load_dotenv()
    # Obtener las variables de entorno
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    db_name = os.getenv("MONGODB_NAME")

    # Construir la URI de conexión
    uri = f"mongodb+srv://{username}:{password}@projectpy.sgszczz.mongodb.net/?retryWrites=true&w=majority&appName={db_name}"

    # Conectar al server
    client = MongoClient(uri)
    db = client['scrapdb']
    collection = db['data']
        
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    return collection