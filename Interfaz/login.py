from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from ConexionDB.usuarios import verificar_credenciales
from PyQt6.QtCore import QTimer  # <--- AÑADIDO: Importar QTimer


class LoginForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        loadUi("ui/ui_login.ui", self)

        # Asegúrate de que el botón de login se llame 'pushButton_login' en tu .ui
        # Si tiene otro nombre (como 'pushButton'), cámbialo aquí.
        try:
            self.pushButton_login.clicked.connect(self.login)
        except AttributeError:
            # Si no se llama 'pushButton_login', quizás se llame 'pushButton'
            print(
                "ADVERTENCIA: No se encontró 'pushButton_login', intentando con 'pushButton'. Revisa tu 'ui_login.ui'.")
            self.pushButton.clicked.connect(self.login)

        self.btn_to_register.clicked.connect(self.go_to_register)

    def login(self):
        user = self.lineEdit_user.text()
        password = self.lineEdit_pass.text()

        if verificar_credenciales(user, password):
            self.label_status.setText(f"Bienvenido, {user}")
            self.label_status.setStyleSheet("color: green;")
            self.label_status.setVisible(True)  # Asegúrate de que sea visible

            # --- LÍNEA CLAVE AÑADIDA (con QTimer) ---
            # Espera 800 milisegundos (0.8 seg) y luego llama a login_exitoso
            QTimer.singleShot(800, self.main_window.login_exitoso)
            # ----------------------------------------

        else:
            self.label_status.setText("Usuario o contraseña incorrectos")
            self.label_status.setStyleSheet("color: red;")
            self.label_status.setVisible(True)  # Asegúrate de que sea visible

    def go_to_register(self):
        self.main_window.cambiar_vista("registro")