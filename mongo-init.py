from pymongo import MongoClient

# Conexión al servidor de MongoDB
client = MongoClient('localhost', 27017)

# Acceso a la base de datos 'admin'
admin_db = client.admin

# Autenticación con el usuario raíz
admin_db.authenticate("maximundl", "a123456!")

# Acceso a la base de datos 'db_dtt'
db = client['db_dtt']

# Creación de usuario
db.command("createUser", "admin", pwd="a123456!", roles=[{"role": "readWrite", "db": "db_dtt"}])

# Creación de colecciones
db.create_COLLECTION("deeplinks")
db.create_COLLECTION("farenet_doc")
db.create_COLLECTION("farenet_doc_ids")
db.create_COLLECTION("farenet_ibe_dataLayer")
db.create_COLLECTION("farenet_ibe_selectors")
db.create_COLLECTION("results")

