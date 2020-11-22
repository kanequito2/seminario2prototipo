import quickhome as qh
import pymongo

def ejecutar(type):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    prestadores = db['prestadores']

    query = {'tipo' : type}
    result = prestadores.find(query)
    response = []
    for x in list(result):
        response.append(
            qh.Prestador(
                x['nombre'],
                x['tipo'],
                x['direccion'],
                x['email'],
                x['celular'],
                x['contrasena'],
                x['calificacion'],
                x['comentarios']
                ))
    return response

def solicitudes(usuario):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    solicitudes = db['servicios']

    query = {'cedula' : usuario.cedula}
    result = solicitudes.find(query)
    
    response = []
    for x in list(result):
        response.append(
            qh.Servicio(
                x['cedula'],
                x['prestador']
            )
        )
    return(response)

def calificar(servicio,calificacion,comentario):

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    prestadores = db['prestadores']

    query = {'nombre' : servicio.prestador}
    operationcomment = {
        '$push' : {
            'comentarios' : comentario
        }
    }
    operationrating = {
        '$push' : {
            'calificacion' : calificacion
        }
    }
    resultc = prestadores.find_one_and_update(query,operationcomment)
    resultr = prestadores.find_one_and_update(query,operationrating)
    print(resultc)
    print(resultr)
    #DELETE QUERY
    if resultc and resultr:
        return True
    else:
        return False
    
def solicitudesprestador(prestador):
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    servicios = db['servicios']
    usuarios = db['usuarios']

    query = {'prestador' : prestador.nombre}
    result = servicios.find(query)
    response = []
    for serv in list(result):
        query = {'cedula' : serv['cedula']}
        user = usuarios.find_one(query)
        response.append(
            qh.Usuario(
                user['nombre'],
                user['cedula'],
                user['email'],
                user['celular'],
                user['contrasena']
            )
        )
    return response