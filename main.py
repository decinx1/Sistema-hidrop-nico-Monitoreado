import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QLabel
)
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt

from Interfaz.home import HomeWindow 
from Interfaz.datos import DatosView 
from Interfaz.sidebar import Sidebar
from Interfaz.botonesheader import BotonesHeader

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
        historial_view = self._create_centered_page("Historial de datos")

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
    
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())