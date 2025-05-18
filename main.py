import sys
import os
from PyQt6.QtCore import QTimer

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QLabel, QDialog, QLineEdit, QPushButton
)
from PyQt6.uic import loadUi
from PyQt6.QtCore import QFile, QIODevice, QTextStream
from PyQt6.QtCore import Qt
from Interfaz.home import HomeWindow 
from Interfaz.datos import DatosView 
from Interfaz.sidebar import Sidebar
from Interfaz.botonesheader import BotonesHeader
from Interfaz.Calendar import CalendarWindow

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join("ui", "ui_login.ui"), self)
        self.setWindowTitle("Inicio de Sesión")
        self.staticUser = "hydroadmin"
        self.staticPass = "123"
        self.pushButton.clicked.connect(self.check_login)
        self.accepted = False

    def check_login(self):
        user = self.lineEdit_user.text()
        password = self.lineEdit_pass.text()
        if user.lower() == self.staticUser.lower() and password == self.staticPass:
            self.label_status.setText(f"Bienvenido, {user}")
            self.label_status.setStyleSheet("color: green;")
            self.accepted = True
            # Espera 1.5 segundos antes de cerrar el login para mostrar el mensaje
            QTimer.singleShot(800, self.accept)
        else:
            self.label_status.setText("Usuario o contraseña incorrectos")
            self.label_status.setStyleSheet("color: red;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HydroTech")

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ─── Área de contenido principal ───────────────────────────
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        sidebar_widget = Sidebar()
        main_layout.addWidget(sidebar_widget)
        
        # Parte superior: botones
        botones_widget = BotonesHeader()
        content_layout.addWidget(botones_widget)

        # Parte inferior: área de vistas
        self.stack = QStackedWidget()
        home_view = HomeWindow()
        datos_view = DatosView()
        historial_view = CalendarWindow()

        self.stack.addWidget(home_view)  # 0
        self.stack.addWidget(datos_view)  # 1
        self.stack.addWidget(historial_view)  # 2

        content_layout.addWidget(self.stack)

        # Conectar los botones para cambiar la vista
        botones_widget.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        botones_widget.btn_datos.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        botones_widget.btn_historial.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # Agrega el área de contenido al layout principal
        main_layout.addWidget(content_widget)

    def on_sidebar_toggled(self, expanded):
    # Aquí podrías hacer que el contenido se expanda o se ajuste
        if expanded:
            print("Sidebar expandida")
        else:
            print("Sidebar retraída")
    
    # Aquí puedes forzar un resize si es necesario
        self.adjustSize()

    def _on_sidebar_toggled_with_message(self, expanded):
        if expanded:
            self.stack.setCurrentIndex(0)  # Home
            print("Home")
        else:
            self.stack.setCurrentIndex(2)  # Configuración
            print("Configuración")

    def _create_centered_page(self, html_text):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel(html_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # --- Cargar Hoja de Estilos ---
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qss_relative_path = os.path.join("access", "qss", "styles.qss")
        qss_path = os.path.abspath(os.path.join(script_dir, qss_relative_path))
        qss_file = QFile(qss_path)
        if not qss_file.exists():
            print(f"ERROR: El archivo de hoja de estilos NO EXISTE en la ruta: {qss_path}")
        elif qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            app.setStyleSheet(stream.readAll())
            qss_file.close()
            print(f"Hoja de estilos '{qss_path}' cargada correctamente.")
        else:
            print(f"ERROR: No se pudo abrir la hoja de estilos '{qss_path}'. Razón: {qss_file.errorString()}")
    except Exception as e:
        print(f"Excepción durante la carga de la hoja de estilos: {e}")
    # --- Fin Carga de Estilos ---

    # Mostrar login antes de la ventana principal
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Accepted and login.accepted:
        window = MainWindow()
        window.showMaximized()
        sys.exit(app.exec())
    else:
        sys.exit(0)