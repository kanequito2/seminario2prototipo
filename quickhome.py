class Usuario():

    def __init__(self,nombre,cedula,email,celular,contrasena):

        self.nombre = nombre
        self.cedula = cedula
        self.email = email
        self.celular = celular
        self.contrasena = contrasena

    def myself(self):

        return {
            'nombre' : self.nombre,
            'cedula' : self.cedula,
            'email' : self.email,
            'celular' : self.celular,
        }
    
    def login(self,ingreso):
        
        if self.contrasena == ingreso:
            return True
        else:
            return False

class Prestador():

    def __init__(self,nombre,tipo,direccion,email,celular,contrasena,calificacion=[],comentarios=[]):

        self.nombre = nombre
        self.tipo = tipo
        self.direccion = direccion
        self.email = email
        self.celular = celular
        self.calificacion = calificacion
        self.comentarios = comentarios
        self.contrasena = contrasena

    def myself(self):

        return {
            'nombre' : self.nombre,
            'tipo' : self.tipo,
            'direccion' : self.direccion,
            'email' : self.email,
            'celular' : self.celular,
            'calificacion' : self.calificacion,
            'comentarios' : self.comentarios
        }
    
    def login(self,ingreso):

        if self.contrasena == ingreso:
            return True
        else:
            return False

class Servicio():

    def __init__(self,usuario,prestador):

        self.usuario = usuario
        self.prestador = prestador
    
    def myself(self):

        return {
            'cedula' : self.usuario,
            'prestador' : self.prestador
        }