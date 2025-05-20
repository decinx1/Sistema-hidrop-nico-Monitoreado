from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from ConexionDB.usuarios import verificar_credenciales

class LoginForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        loadUi("ui_login.ui", self)

        self.pushButton.clicked.connect(self.login)
        self.btn_to_register.clicked.connect(self.go_to_register)

    def login(self):
        user = self.lineEdit_user.text()
        password = self.lineEdit_pass.text()

        if verificar_credenciales(user, password):
            self.label_status.setText(f"Bienvenido, {user}")
            self.label_status.setStyleSheet("color: green;")
        else:
            self.label_status.setText("Usuario o contraseña incorrectos")
            self.label_status.setStyleSheet("color: red;")

    def go_to_register(self):
        self.main_window.cambiar_vista("registro")
