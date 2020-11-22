import quickhome as qh
import pymongo

def ejecutar(prestador,usuario):
    print(prestador.myself())
    print(usuario.myself())

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    servicios = db['servicios']

    servicio = qh.Servicio(
        usuario.cedula,
        prestador.nombre
    )

    query = {'$and' : [
        {'cedula' : servicio.usuario},
        {'prestador' : servicio.prestador}
    ]}
    result = servicios.find_one(query)
    if result:
        return False
    else:
        servicios.insert(servicio.myself())
        return True