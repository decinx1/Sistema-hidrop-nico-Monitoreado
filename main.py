import sys
import os
from PyQt6.QtCore import QTimer

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QLabel, QDialog
)
from PyQt6.QtCore import QFile, QIODevice, QTextStream
from PyQt6.QtCore import Qt

# Importar solo LoginForm
from Interfaz.login import LoginForm


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.staticUser = "hydroadmin"
        self.staticPass = "123"
        self.accepted = False

        # Crear widgets manualmente
        layout = QVBoxLayout(self)
        self.label_title = QLabel("Inicio de Sesión")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.label_title)

        self.lineEdit_user = QLabel("Usuario:")
        layout.addWidget(self.lineEdit_user)
        self.input_user = QWidget()
        from PyQt6.QtWidgets import QLineEdit
        self.lineEdit_user = QLineEdit()
        layout.addWidget(self.lineEdit_user)

        self.lineEdit_pass_label = QLabel("Contraseña:")
        layout.addWidget(self.lineEdit_pass_label)
        self.lineEdit_pass = QLineEdit()
        self.lineEdit_pass.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.lineEdit_pass)

        from PyQt6.QtWidgets import QPushButton
        self.pushButton = QPushButton("Iniciar sesión")
        layout.addWidget(self.pushButton)
        self.label_status = QLabel("")
        self.label_status.setStyleSheet("color: red;")
        layout.addWidget(self.label_status)

        self.pushButton.clicked.connect(self.check_login)

    def check_login(self):
        user = self.lineEdit_user.text()
        password = self.lineEdit_pass.text()
        if user.lower() == self.staticUser.lower() and password == self.staticPass:
            self.label_status.setText(f"Bienvenido, {user}")
            self.label_status.setStyleSheet("color: green;")
            self.accepted = True
        else:
            self.label_status.setText("Usuario o contraseña incorrectos")
            self.label_status.setStyleSheet("color: red;")


class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login y Registro")
        self.setFixedSize(400, 400)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        # Usar solo LoginForm
        self.login_form = LoginForm(self)
        self.stack.addWidget(self.login_form)  # índice 0
        self.stack.setCurrentIndex(0)

        self.main_app_window = None  # <--- AÑADIDO: Para guardar la ventana principal

    def cambiar_vista(self, vista):
        if vista == "login":
            self.stack.setCurrentIndex(0)

    # <--- MÉTODO AÑADIDO --- >
    def login_exitoso(self):
        """Esta función se llamará cuando el login sea correcto."""
        print("Login exitoso! Abriendo aplicación principal...")
        self.main_app_window = MainWindow()  # Creamos la ventana principal
        self.main_app_window.showMaximized()  # La mostramos (o .show() si prefieres tamaño normal)
        self.close()  # Cerramos la ventana de Auth/Login
    # <--- FIN MÉTODO AÑADIDO --- >


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HydroTech")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Sidebar con importación bajo demanda
        from Interfaz.sidebar import Sidebar
        sidebar_widget = Sidebar()
        main_layout.addWidget(sidebar_widget)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        # BotonesHeader con importación bajo demanda
        from Interfaz.botonesheader import BotonesHeaderUI
        self.botones_widget = BotonesHeaderUI()
        content_layout.addWidget(self.botones_widget)
        self.stack = QStackedWidget()
        self.views = {}  # Diccionario para lazy loading
        # SOLO carga la vista inicial (Home) al inicio, no todas
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_widget)
        # Conectar solo los botones de BotonesHeader a las vistas que lo requieren
        self.botones_widget.btnHome.clicked.connect(lambda: self._load_view(0))
        self.botones_widget.btnDatos.clicked.connect(lambda: self._load_view(1))
        self.botones_widget.btnHistorial.clicked.connect(lambda: self._load_view(2))
        # Conectar Sidebar a las vistas (solo Home, Datos, Historial)
        sidebar_widget._btns["Home"].clicked.connect(lambda: self._show_view_with_header(0))
        sidebar_widget._btns["Datos"].clicked.connect(lambda: self._show_view_with_header(1))
        sidebar_widget._btns["Historial"].clicked.connect(lambda: self._show_view_with_header(2))
        # Carga la vista inicial (Home) después de conectar los botones
        # Muestra un mensaje de carga bonito mientras se inicializa HomeWindow
        self.loading_widget = QWidget()
        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label = QLabel("<b>Cargando panel principal...</b>")
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_label.setStyleSheet("font-size: 22px; color: #16A34A; margin-bottom: 16px;")
        
        loading_layout.addWidget(loading_label)
        self.stack.addWidget(self.loading_widget)
        self.stack.setCurrentWidget(self.loading_widget)
        QTimer.singleShot(100, self._load_home_async)

    def _load_home_async(self):
        from Interfaz.home import HomeWindow
        view = HomeWindow()
        self.views[0] = view
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)
        # Elimina el mensaje de carga
        self.stack.removeWidget(self.loading_widget)
        self.loading_widget.deleteLater()

    def _show_view_with_header(self, index):
        self.botones_widget.show()
        self._load_view(index)

    def _show_view_without_header(self, index):
        self.botones_widget.hide()
        self._load_view(index)

    def _load_view(self, index):
        if hasattr(self, '_loading_view') and self._loading_view:
            return  # Ya se está cargando una vista, ignora clicks rápidos
        self._loading_view = True
        try:
            if index not in self.views:
                if index == 0:
                    from Interfaz.home import HomeWindow
                    view = HomeWindow()
                elif index == 1:
                    from Interfaz.datos import DatosView
                    view = DatosView()
                elif index == 2:
                    from Interfaz.Calendar import CalendarWindow
                    view = CalendarWindow()
                else:
                    self._loading_view = False
                    return
                self.views[index] = view
                self.stack.addWidget(view)
            self.stack.setCurrentWidget(self.views[index])
        finally:
            self._loading_view = False

    def on_sidebar_toggled(self, expanded):
        if expanded:
            print("Sidebar expandida")
        else:
            print("Sidebar retraída")
        # Aquí podrías hacer que el contenido se expanda o se ajuste
        self.adjustSize()

    def _on_sidebar_toggled_with_message(self, expanded):
        if expanded:
            self.stack.setCurrentIndex(0)  # Home
            print("Home")
        else:
            self.stack.setCurrentIndex(1)  # Datos
            print("Datos")

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
        if qss_file.exists() and qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            app.setStyleSheet(stream.readAll())
            qss_file.close()
            print(f"Hoja de estilos '{qss_path}' cargada correctamente.")
        else:
            print(f"ERROR: El archivo de hoja de estilos NO EXISTE o no se pudo abrir en la ruta: {qss_path}")
    except Exception as e:
        print(f"Excepción durante la carga de la hoja de estilos: {e}")
    # --- Fin Carga de Estilos ---

    # Mostrar ventana de login/registro y luego dashboard
    # auth = AuthWindow()
    # auth.show()
    # app.exec()
    # Para pruebas sin login, puedes iniciar el dashboard directamente:
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec()