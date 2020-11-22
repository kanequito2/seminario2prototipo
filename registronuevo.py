import quickhome as qh
import pymongo

def registrar(usuario):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    users = db['usuarios']

    query = {'cedula' : usuario.cedula}
    result = users.find_one(query)
    if result:
        return False
    else:
        nuevo = usuario.myself()
        nuevo['contrasena'] = usuario.contrasena
        users.insert_one(nuevo)
        return True