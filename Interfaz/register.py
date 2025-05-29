from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from ConexionDB.usuarios import registrar_usuario
from Interfaz.tokenSMS import enviar_codigo_verificacion, verificar_codigo

class RegisterForm(QWidget):
    lada_max_digitos = {
        "+52": 10, "+1": 10, "+54": 10, "+55": 11, "+56": 9, "+57": 10,
        "+51": 9, "+58": 10, "+598": 8, "+593": 9, "+591": 8, "+595": 9,
        "+506": 8, "+502": 8, "+504": 8, "+505": 8, "+503": 8, "+507": 8,
        "+34": 9, "+33": 9, "+39": 10,
    }

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        # Título
        label_title = QLabel("Registro de Usuario")
        label_title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_title)
        # Nombre
        self.lineEdit_nombre = QLineEdit()
        self.lineEdit_nombre.setPlaceholderText("Nombre completo")
        layout.addWidget(self.lineEdit_nombre)
        # Lada y teléfono
        lada_tel_layout = QHBoxLayout()
        self.comboBox_lada = QComboBox()
        self.comboBox_lada.setFixedWidth(120)
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/mx.svg"), "+52 México")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/us.svg"), "+1 USA")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/ar.svg"), "+54 Argentina")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/br.svg"), "+55 Brasil")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/cl.svg"), "+56 Chile")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/co.svg"), "+57 Colombia")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/pe.svg"), "+51 Perú")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/ve.svg"), "+58 Venezuela")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/uy.svg"), "+598 Uruguay")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/ec.svg"), "+593 Ecuador")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/bo.svg"), "+591 Bolivia")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/py.svg"), "+595 Paraguay")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/cr.svg"), "+506 Costa Rica")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/gt.svg"), "+502 Guatemala")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/hn.svg"), "+504 Honduras")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/ni.svg"), "+505 Nicaragua")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/sv.svg"), "+503 El Salvador")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/pa.svg"), "+507 Panamá")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/es.svg"), "+34 España")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/fr.svg"), "+33 Francia")
        self.comboBox_lada.addItem(QIcon("Interfaz/flags/it.svg"), "+39 Italia")
        lada_tel_layout.addWidget(self.comboBox_lada)
        self.lineEdit_telefono = QLineEdit()
        self.lineEdit_telefono.setPlaceholderText("Teléfono")
        lada_tel_layout.addWidget(self.lineEdit_telefono)
        layout.addLayout(lada_tel_layout)
        # Código de verificación
        self.lineEdit_codigo_verificacion = QLineEdit()
        self.lineEdit_codigo_verificacion.setPlaceholderText("Código de verificación")
        layout.addWidget(self.lineEdit_codigo_verificacion)
        # Contraseña
        self.lineEdit_contraseña = QLineEdit()
        self.lineEdit_contraseña.setPlaceholderText("Contraseña")
        self.lineEdit_contraseña.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.lineEdit_contraseña)
        # Botones de verificación y registro
        btns_layout = QHBoxLayout()
        self.pushButton_enviar_codigo = QPushButton("Enviar código")
        btns_layout.addWidget(self.pushButton_enviar_codigo)
        self.pushButton_verificar_codigo = QPushButton("Verificar código")
        btns_layout.addWidget(self.pushButton_verificar_codigo)
        layout.addLayout(btns_layout)
        self.pushButton_registrar = QPushButton("Registrar")
        layout.addWidget(self.pushButton_registrar)
        self.btn_to_login = QPushButton("Volver al login")
        layout.addWidget(self.btn_to_login)
        # Resultado
        self.label_resultado = QLabel("")
        self.label_resultado.setVisible(False)
        layout.addWidget(self.label_resultado)
        # Conexiones
        self.comboBox_lada.currentIndexChanged.connect(self.actualizar_max_digitos)
        self.actualizar_max_digitos()
        self.codigo_verificado = False
        self.pushButton_enviar_codigo.clicked.connect(self.enviar_codigo)
        self.pushButton_verificar_codigo.clicked.connect(self.verificar_codigo)
        self.pushButton_registrar.clicked.connect(self.registrar)
        self.btn_to_login.clicked.connect(self.go_to_login)

    def actualizar_max_digitos(self):
        lada = self.comboBox_lada.currentText().split()[0]
        max_digitos = self.lada_max_digitos.get(lada, 10)
        self.lineEdit_telefono.setMaxLength(max_digitos)

    def enviar_codigo(self):
        lada = self.comboBox_lada.currentText().split()[0]
        telefono = self.lineEdit_telefono.text()
        telefono_completo = f"{lada}{telefono}"
        self.codigo_verificado = False
        if not telefono:
            self.label_resultado.setText("Ingresa el teléfono")
            self.label_resultado.setStyleSheet("color: red;")
            self.label_resultado.setVisible(True)
            return
        try:
            enviar_codigo_verificacion(telefono_completo)
            self.label_resultado.setText("Código enviado por SMS")
            self.label_resultado.setStyleSheet("color: green;")
            self.label_resultado.setVisible(True)
        except Exception:
            self.label_resultado.setText("Error al enviar SMS")
            self.label_resultado.setStyleSheet("color: red;")
            self.label_resultado.setVisible(True)

    def verificar_codigo(self):
        lada = self.comboBox_lada.currentText().split()[0]
        telefono = self.lineEdit_telefono.text()
        telefono_completo = f"{lada}{telefono}"
        codigo = self.lineEdit_codigo_verificacion.text()
        if verificar_codigo(telefono_completo, codigo):
            self.codigo_verificado = True
            self.label_resultado.setText("Código verificado correctamente")
            self.label_resultado.setStyleSheet("color: green;")
        else:
            self.codigo_verificado = False
            self.label_resultado.setText("Código incorrecto")
            self.label_resultado.setStyleSheet("color: red;")

    def registrar(self):
        nombre = self.lineEdit_nombre.text()
        lada = self.comboBox_lada.currentText().split()[0]
        telefono = self.lineEdit_telefono.text()
        telefono_completo = f"{lada}{telefono}"
        contraseña = self.lineEdit_contraseña.text()

        if not self.codigo_verificado:
            self.label_resultado.setText("Verifica el código antes de registrar")
            self.label_resultado.setStyleSheet("color: red;")
            return

        if not nombre or not telefono or not contraseña:
            self.label_resultado.setText("Todos los campos son obligatorios")
            self.label_resultado.setStyleSheet("color: red;")
            return

        if registrar_usuario(nombre, telefono_completo, contraseña):
            self.label_resultado.setText("Usuario registrado correctamente")
            self.label_resultado.setStyleSheet("color: green;")
            self.limpiar()
        else:
            self.label_resultado.setText("Error al registrar usuario")
            self.label_resultado.setStyleSheet("color: red;")

    def limpiar(self):
        self.lineEdit_nombre.clear()
        self.lineEdit_telefono.clear()
        self.lineEdit_contraseña.clear()

    def go_to_login(self):
        self.main_window.cambiar_vista("login")