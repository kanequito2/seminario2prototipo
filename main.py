import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QMessageBox, QDesktopWidget, QComboBox, QListWidget
)
from PyQt5.QtGui import QPixmap
from numpy import average

import quickhome as qh
import ingreso
import registroprestador as rp
import registronuevo as rg
import buscar
import solicitar

class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(300,300)
        rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())
        self.setWindowTitle('QUICKHOME')

        mainlay = QVBoxLayout()
        
        self.logolabel = QLabel(self)
        self.pixmap = QPixmap('logo.png')
        # self.pixmap = self.pixmap.scaledToHeight(80)
        self.logolabel.setPixmap(self.pixmap)
        logolay = QHBoxLayout()
        logolay.addWidget(self.logolabel)
        self.logolabel.setAlignment(Qt.AlignCenter)
        mainlay.addLayout(logolay)

        self.namelabel = QLabel('Cedula/Nombre:')
        self.nameentry = QLineEdit(self)
        self.namelabel.setBuddy(self.nameentry)
        namelayout = QHBoxLayout()
        namelayout.addWidget(self.namelabel)
        namelayout.addWidget(self.nameentry)
        mainlay.addLayout(namelayout)

        self.passwordlabel = QLabel('Contrasena:')
        self.passwordentry = QLineEdit(self)
        self.passwordentry.setEchoMode(QLineEdit.Password)
        self.passwordlabel.setBuddy(self.passwordentry)
        passlayout = QHBoxLayout()
        passlayout.addWidget(self.passwordlabel)
        passlayout.addWidget(self.passwordentry)
        mainlay.addLayout(passlayout)

        self.login = QPushButton('INGRESAR')
        self.register = QPushButton('REGISTRAR')
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.login)
        buttonlayout.addWidget(self.register)
        self.login.clicked.connect(self.loginf)
        self.register.clicked.connect(self.registerf)
        mainlay.addLayout(buttonlayout)

        self.closer = QPushButton('EXIT')
        self.closer.clicked.connect(self.kill)
        mainlay.addWidget(self.closer)

        self.setLayout(mainlay)

    def kill(self):
            self.close()

    def loginf(self):
        response = ingreso.ingresar(
            self.nameentry.text(),
            self.passwordentry.text()
        )
        if response[0] == 3:
            self.prestadorin = PrestadorIn(response[1])
            self.prestadorin.show()
        elif response[0] == 2:
            self.adminwindow = Admin()
            self.adminwindow.show()
        elif response[0] == 1:
            self.ingresado = UserIn(response[1])
            self.ingresado.show()
        elif response[0] == 0:
            QMessageBox.about(self,'ERROR','Contraseña equivocada.')
        else:
            QMessageBox.about(self,'ERROR','El usuario no existe.')


    def registerf(self):
        self.registergui = RegisterGUI()
        self.registergui.show()
########################################
class PrestadorIn(QWidget):

    def __init__(self,prestador):
        self.prestador = prestador
        super().__init__()
        self.resize(200,200)
        self.move(200,100)
        self.setWindowTitle('BIENVENIDO ' + prestador.nombre)   

        mainlay = QVBoxLayout()

        self.solicitudes = QListWidget(self)
        opciones = buscar.solicitudesprestador(self.prestador)
        opciones = [(x.nombre + '\t' + x.celular) for x in opciones]
        self.solicitudes.insertItems(0,['Nombre\tCelular'])
        self.solicitudes.insertItems(1,opciones)
        mainlay.addWidget(self.solicitudes)

        self.closebutton = QPushButton('CERRAR')
        self.closebutton.clicked.connect(self.close)
        mainlay.addWidget(self.closebutton)

        self.setLayout(mainlay)
########################################
class UserIn(QWidget):

    def __init__(self,user):
        super().__init__()
        self.resize(300,300)
        self.move(200,100)
        self.setWindowTitle('BIENVENIDO ' + user.nombre)
        self.user = user

        mainlay = QVBoxLayout()

        self.b00 = QPushButton('ESTILISTA')
        self.b01 = QPushButton('ESTECISISTA')
        self.b10 = QPushButton('MANICURISTA')
        self.b11 = QPushButton('NUTRICIONISTA')
        self.b20 = QPushButton('MASAJISTA')
        self.b21 = QPushButton('ENTRENADOR')
        self.b00.clicked.connect(lambda: self.buttonpress(self.b00.text().lower()))
        self.b01.clicked.connect(lambda: self.buttonpress(self.b01.text().lower()))
        self.b10.clicked.connect(lambda: self.buttonpress(self.b10.text().lower()))
        self.b11.clicked.connect(lambda: self.buttonpress(self.b11.text().lower()))
        self.b20.clicked.connect(lambda: self.buttonpress(self.b20.text().lower()))
        self.b21.clicked.connect(lambda: self.buttonpress(self.b21.text().lower()))
        r0 = QHBoxLayout()
        r0.addWidget(self.b00)
        r0.addWidget(self.b01)
        r1 = QHBoxLayout()
        r1.addWidget(self.b10)
        r1.addWidget(self.b11)
        r2 = QHBoxLayout()
        r2.addWidget(self.b20)
        r2.addWidget(self.b21)
        
        self.mysolicitudes = QPushButton('MIS SOLICITUDES')
        self.mysolicitudes.clicked.connect(self.missolicitudes)
        self.closebutton = QPushButton('CERRAR')
        self.closebutton.clicked.connect(self.close)

        mainlay.addLayout(r0)
        mainlay.addLayout(r1)
        mainlay.addLayout(r2)
        mainlay.addWidget(self.mysolicitudes)
        mainlay.addWidget(self.closebutton)

        self.setLayout(mainlay)

    def buttonpress(self,text):
        response = buscar.ejecutar(text)
        self.solicitar = Solicitar(self.user,response,text)
        self.solicitar.show()
    
    def missolicitudes(self):
        result = buscar.solicitudes(self.user)
        self.miss = MisSolicitudes(self.user,result)
        self.miss.show()
    
########################################
class MisSolicitudes(QWidget):

    def __init__(self,user,servicios):
        super().__init__()
        self.user = user
        self.servicios = servicios
        self.resize(250,250)
        self.move(200,100)
        self.setWindowTitle('MIS SOLICITUDES')

        mainlay = QVBoxLayout()

        self.solicitudes = QComboBox(self)
        if len(self.servicios) > 0:
            opciones = []
            for x in self.servicios:
                opciones.append(x.prestador)
            self.solicitudes.insertItems(0,opciones)
            self.solicitudes.setCurrentIndex(0)
        mainlay.addWidget(self.solicitudes)

        self.ratelabel = QLabel('Calificacion:')
        self.rateinput = QComboBox(self)
        self.rateinput.insertItems(0,[str(x) for x in range(1,6)])
        self.rateinput.setCurrentIndex(0)
        ratelay = QHBoxLayout()
        ratelay.addWidget(self.ratelabel)
        ratelay.addWidget(self.rateinput)
        mainlay.addLayout(ratelay)

        self.commentlabel = QLabel('Comentario')
        self.commentinpupt = QLineEdit(self)
        commentlay = QHBoxLayout()
        commentlay.addWidget(self.commentlabel)
        commentlay.addWidget(self.commentinpupt)
        mainlay.addLayout(commentlay)

        self.completarbutton = QPushButton('COMPLETAR')
        self.cancelbutton = QPushButton('CANCELAR')
        self.completarbutton.clicked.connect(self.completar)
        self.cancelbutton.clicked.connect(self.close)
        mainlay.addWidget(self.completarbutton)
        mainlay.addWidget(self.cancelbutton)


        self.setLayout(mainlay)

    def completar(self):
        
        response = buscar.calificar(
            self.servicios[self.solicitudes.currentIndex()],
            int(self.rateinput.currentText()),
            self.commentinpupt.text()
        )
        if response:
            QMessageBox.about(self,'EXITO','Gracias por su\ncalificacion.')
            self.close()
        else:
            QMessageBox.about(self,'ERROR','ERROR')

########################################
class Solicitar(QWidget):

    def __init__(self,user,prestadores,text):
        super().__init__()
        self.user = user
        self.prestadores = prestadores
        self.resize(200,250)
        self.move(200,100)
        self.setWindowTitle('SOLICITAR')
        
        mainlay = QVBoxLayout()
        
        self.aquevino = QLabel(text.upper() + ' DISPONIBLES')
        self.aquevino.setAlignment(Qt.AlignCenter)
        mainlay.addWidget(self.aquevino)
        self.lista = QComboBox(self)
        mainlay.addWidget(self.lista)

        if not len(self.prestadores) == 0:

            opciones = []
            for p in self.prestadores:
                opciones.append(p.nombre)
            
            self.lista.insertItems(0,opciones)
            self.lista.setCurrentIndex(0)
            self.lista.currentIndexChanged.connect(self.changeshit)

            self.dirlabel = QLabel('Direccion:')
            self.dirinfo = QLabel(self.prestadores[0].direccion)
            dirlay = QHBoxLayout()
            dirlay.addWidget(self.dirlabel)
            dirlay.addWidget(self.dirinfo)
            mainlay.addLayout(dirlay)

            self.emaillabel = QLabel('Correo:')
            self.emailinfo = QLabel(self.prestadores[0].email)
            emaillay = QHBoxLayout()
            emaillay.addWidget(self.emaillabel)
            emaillay.addWidget(self.emailinfo)
            mainlay.addLayout(emaillay)

            self.cellabel = QLabel('Celular:')
            self.celinfo = QLabel(self.prestadores[0].celular)
            cellay = QHBoxLayout()
            cellay.addWidget(self.cellabel)
            cellay.addWidget(self.celinfo)
            mainlay.addLayout(cellay)

            rating = '-/-'
            self.ratelabel = QLabel('Calificaion:')
            if len(self.prestadores[0].calificacion) > 0:
                rating = str(average(
                    [int(x) for x in self.prestadores[0].calificacion]
                ))
            self.rateinfo = QLabel(rating)
            ratelay = QHBoxLayout()
            ratelay.addWidget(self.ratelabel)
            ratelay.addWidget(self.rateinfo)
            mainlay.addLayout(ratelay)

            self.comments = QListWidget(self)
            if len(self.prestadores[0].comentarios) > 0:
                self.comments.insertItems(0,self.prestadores[0].comentarios)
            else:
                self.comments.insertItems(0,['-----NO HAY COMENTARIOS-----'])

            commentlay = QHBoxLayout()
            commentlay.addWidget(self.comments)
            commentlay.setAlignment(Qt.AlignCenter)
            mainlay.addLayout(commentlay)

            self.solicitarbutton = QPushButton('SOLICITAR')
            self.solicitarbutton.clicked.connect(self.solicitar)
            mainlay.addWidget(self.solicitarbutton)
        
        else:
            self.empty = QLabel('NO HAY PRESTADORES\nDISPONIBLES PARA USTED')
            self.empty.setAlignment(Qt.AlignCenter)
            mainlay.addWidget(self.empty)
        
        self.cancelarbutton = QPushButton('CANCELAR')
        self.cancelarbutton.clicked.connect(self.close)
        mainlay.addWidget(self.cancelarbutton)
        
        self.setLayout(mainlay)
    
    def solicitar(self):
        
        response = solicitar.ejecutar(
            self.prestadores[self.lista.currentIndex()],
            self.user
        )
        if response:
            QMessageBox.about(self,'EXITO','Se registro la solicitud')
        else:
            QMessageBox.about(self,'ERROR','Ya tiene una solicitud\ncon este prestador.')
    
    def changeshit(self):
        i = self.lista.currentIndex()
        self.dirinfo.setText(self.prestadores[i].direccion)
        self.emailinfo.setText(self.prestadores[i].email)
        self.celinfo.setText(self.prestadores[i].celular)
        rating = '-/-'
        if len(self.prestadores[i].calificacion) > 0:
            rating = str(average(
                    [int(x) for x in self.prestadores[i].calificacion]
                ))
        self.rateinfo.setText(rating)
        self.comments.clear()
        if len(self.prestadores[i].comentarios) > 0:
            self.comments.insertItems(0,self.prestadores[i].comentarios)
        else:
            self.comments.insertItems(0,['-----NO HAY COMENTARIOS-----'])
            

########################################
class RegisterGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.resize(300,200)
        rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())
        self.setWindowTitle('REGISTRARSE - QUICKHOME')

        mainlay = QVBoxLayout()

        self.titlelabel = QLabel('---NUEVO USUARIO---')
        self.titlelabel.setAlignment(Qt.AlignCenter)
        titlelay = QHBoxLayout()
        titlelay.addWidget(self.titlelabel)
        mainlay.addLayout(titlelay)

        self.namelabel = QLabel('Nombre:')
        self.nameentry = QLineEdit(self)
        namelay = QHBoxLayout()
        namelay.addWidget(self.namelabel)
        namelay.addWidget(self.nameentry)
        mainlay.addLayout(namelay)

        self.cedulalabel = QLabel('Cedula:')
        self.cedulaentry = QLineEdit(self)
        cedulalay = QHBoxLayout()
        cedulalay.addWidget(self.cedulalabel)
        cedulalay.addWidget(self.cedulaentry)
        mainlay.addLayout(cedulalay)

        self.passwordlabel = QLabel('Contraseña:')
        self.passwordentry = QLineEdit(self)
        self.passwordentry.setEchoMode(QLineEdit.Password)
        passlayout = QHBoxLayout()
        passlayout.addWidget(self.passwordlabel)
        passlayout.addWidget(self.passwordentry)
        mainlay.addLayout(passlayout)

        self.emaillabel = QLabel('Email:')
        self.emailentry = QLineEdit(self)
        emaillay = QHBoxLayout()
        emaillay.addWidget(self.emaillabel)
        emaillay.addWidget(self.emailentry)
        mainlay.addLayout(emaillay)

        self.celularlabel = QLabel('Celular:')
        self.celularentry = QLineEdit(self)
        celularlay = QHBoxLayout()
        celularlay.addWidget(self.celularlabel)
        celularlay.addWidget(self.celularentry)
        mainlay.addLayout(celularlay)

        self.registrarbutton = QPushButton('REGISTRAR')
        self.cancelarbutton = QPushButton('CANCELAR')
        buttonlay = QHBoxLayout()
        buttonlay.addWidget(self.registrarbutton)
        buttonlay.addWidget(self.cancelarbutton)
        self.registrarbutton.clicked.connect(self.register)
        self.cancelarbutton.clicked.connect(self.kill)
        mainlay.addLayout(buttonlay)

        self.setLayout(mainlay)

    def kill(self):
        self.close()
    
    def register(self):
        usuario = qh.Usuario(
            self.nameentry.text(),
            self.cedulaentry.text(),
            self.emailentry.text(),
            self.celularentry.text(),
            self.passwordentry.text()
        )
        response = rg.registrar(usuario)
        if response:
            QMessageBox.about(self,'EXITO','Usuario registrado')
            self.close()
        else:
            QMessageBox.about(self,'ERROR','Ya existe la cedula')

########################################
class Admin(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(250,300)
        self.setWindowTitle('PRESTADORES - QUICKHOME')
        self.move(100,100)

        mainlay = QVBoxLayout()

        self.nombrelabel = QLabel('Nombre:')
        self.nombreentry = QLineEdit(self)
        namelay = QHBoxLayout()
        namelay.addWidget(self.nombrelabel)
        namelay.addWidget(self.nombreentry)
        mainlay.addLayout(namelay)

        tipos = [
            'estilista',
            'estecisista',
            'nutricionista',
            'masajista',
            'entrenador',
            'manicurista'
            ]
        self.tipolabel = QLabel('Tipo:')
        self.tipoentry = QComboBox(self)
        self.tipoentry.insertItems(0,tipos)
        self.tipoentry.setCurrentIndex(0)
        tipolay = QHBoxLayout()
        tipolay.addWidget(self.tipolabel)
        tipolay.addWidget(self.tipoentry)
        mainlay.addLayout(tipolay)

        self.direccionlabel = QLabel('Direccion:')
        self.direccionentry = QLineEdit(self)
        dirlay = QHBoxLayout()
        dirlay.addWidget(self.direccionlabel)
        dirlay.addWidget(self.direccionentry)
        mainlay.addLayout(dirlay)

        self.emaillabel = QLabel('Email:')
        self.emailentry = QLineEdit(self)
        emaillay = QHBoxLayout()
        emaillay.addWidget(self.emaillabel)
        emaillay.addWidget(self.emailentry)
        mainlay.addLayout(emaillay)

        self.cellabel = QLabel('Celular:')
        self.celentry = QLineEdit(self)
        cellay = QHBoxLayout()
        cellay.addWidget(self.cellabel)
        cellay.addWidget(self.celentry)
        mainlay.addLayout(cellay)

        self.passwordlabel = QLabel('Contrasena:')
        self.passwordentry = QLineEdit(self)
        self.passwordentry.setEchoMode(QLineEdit.Password)
        passlayout = QHBoxLayout()
        passlayout.addWidget(self.passwordlabel)
        passlayout.addWidget(self.passwordentry)
        mainlay.addLayout(passlayout)

        self.registrarbutton = QPushButton('REGISTRAR')
        self.cancelbutton = QPushButton('CANCELAR')
        self.registrarbutton.clicked.connect(self.register)
        self.cancelbutton.clicked.connect(self.kill)
        buttonlay = QHBoxLayout()
        buttonlay.addWidget(self.registrarbutton)
        buttonlay.addWidget(self.cancelbutton)
        mainlay.addLayout(buttonlay)


        self.setLayout(mainlay)

    def kill(self):
        self.close()
    
    def register(self):
        prestador = qh.Prestador(
            self.nombreentry.text(),
            self.tipoentry.currentText(),
            self.direccionentry.text(),
            self.emailentry.text(),
            self.celentry.text(),
            self.passwordentry.text()
        )
        response = rp.ejecutar(prestador)
        if response:
            QMessageBox.about(self,'EXITO','Se ha registrado el prestador')
        else:
            QMessageBox.about(self,'ERROR','Ya existe con ese nombre')

######################################
app = QApplication(sys.argv)
w = Main()
w.show()
app.exec_()