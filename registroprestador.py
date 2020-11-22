import quickhome as qh
import pymongo

def ejecutar(prestador):
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    users = db['prestadores']

    query = {'nombre' : prestador.nombre}
    result = users.find_one(query)

    if result:
        return False
    else:
        nuevo = prestador.myself()
        nuevo['contrasena'] = prestador.contrasena
        users.insert_one(nuevo)
        return True