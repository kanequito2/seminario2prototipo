import quickhome as qh
import pymongo

def ingresar(credencial,contrasena):
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['quickhome']
    users = db['usuarios']

    query = {'cedula' : credencial}
    result = users.find_one(query)

    if result:

        if result['contrasena'] == contrasena:

            if result['cedula'] == '123':
                
                return (2,qh.Usuario(
                result['nombre'],
                result['cedula'],
                result['email'],
                result['celular'],
                result['contrasena']
            ))

            return (1,qh.Usuario(
                result['nombre'],
                result['cedula'],
                result['email'],
                result['celular'],
                result['contrasena']
            ))
        else:
            return (0,None)
    
    else:

        query = {'nombre' : credencial}
        prestadores = db['prestadores']
        result = prestadores.find_one(query)
        if result:

            if result['contrasena'] == contrasena:
                return(3,qh.Prestador(
                    result['nombre'],
                    result['tipo'],
                    result['direccion'],
                    result['email'],
                    result['celular'],
                    result['contrasena']
                ))
            else:
                return (0,None)
        
        else:

            return(-1,None)