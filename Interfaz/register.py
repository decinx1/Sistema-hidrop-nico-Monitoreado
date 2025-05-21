from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from ConexionDB.usuarios import registrar_usuario
import os
class RegisterForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'ui_register.ui')
        loadUi(ui_path, self)

        self.pushButton_registrar.clicked.connect(self.registrar)
        self.btn_to_login.clicked.connect(self.go_to_login)

    def registrar(self):
        nombre = self.lineEdit_nombre.text()
        correo = self.lineEdit_correo.text()
        telefono = self.lineEdit_telefono.text()
        contraseña = self.lineEdit_contraseña.text()

        if not nombre or not correo or not telefono or not contraseña:
            self.label_resultado.setText("Todos los campos son obligatorios")
            self.label_resultado.setStyleSheet("color: red;")
            return

        if registrar_usuario(nombre, correo, telefono, contraseña):
            self.label_resultado.setText("Usuario registrado correctamente")
            self.label_resultado.setStyleSheet("color: green;")
            self.limpiar()
        else:
            self.label_resultado.setText("Error al registrar usuario")
            self.label_resultado.setStyleSheet("color: red;")

    def limpiar(self):
        self.lineEdit_nombre.clear()
        self.lineEdit_correo.clear()
        self.lineEdit_telefono.clear()
        self.lineEdit_contraseña.clear()

    def go_to_login(self):
        self.main_window.cambiar_vista("login")
