from bson import ObjectId

#Funcion para serializar ObjectId a str para JSON
def default_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type not serializable")