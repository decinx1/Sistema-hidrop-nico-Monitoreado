import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.uic import loadUi

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Cargar el archivo .ui
        loadUi("ui_login.ui", self)

        # Conectar botón
        self.pushButton.clicked.connect(self.check_login)

        # Cargar credenciales desde env/config.json
        self.load_credentials()

    def load_credentials(self):
        config_path = os.path.join("env", "config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                self.staticUser = config.get("user", "")
                self.staticPass = config.get("password", "")
        except Exception as e:
            print(f"Error al cargar las credenciales: {e}")
            self.staticUser = ""
            self.staticPass = ""

    def check_login(self):
        user = self.lineEdit_user.text()
        password = self.lineEdit_pass.text()

        if user.lower() == self.staticUser.lower() and password == self.staticPass:
            self.label_status.setText(f"Bienvenido, {user}")
            self.label_status.setStyleSheet("color: green;")
        else:
            self.label_status.setText("Usuario o contraseña incorrectos")
            self.label_status.setStyleSheet("color: red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
