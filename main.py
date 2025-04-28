import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QLabel
)
from PyQt6.QtCore import Qt

from sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hydrotech")

        # Widget central y layout horizontal
        central = QWidget()
        central.setObjectName("centralwidget")
        self.setCentralWidget(central)
        hbox = QHBoxLayout(central)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        # Define los ítems del menú: (Texto, nombre_de_icono)
        items = [
            ("Home",          "home.png"),
            ("Configuración", "config.png"),
            ("Usuario",       "Usuario.png"),
            ("Correo",        "Correoo.png"),
            ("Notificaciones","notii.png"),
        ]

        # Instancia la sidebar
        sidebar = Sidebar(
            icon_folder=os.path.join(os.path.dirname(__file__), "icons"),
            menu_items=items,
            expanded_width=180,
            collapsed_width=60,
            animation_duration=180,
            logo_filename="Logeishon.png"
        )
        hbox.addWidget(sidebar)

        # Área de contenido con QStackedWidget
        self.stack = QStackedWidget()
        for name, _ in items:
            page = self._create_centered_page(f"<h1>{name}</h1>")
            self.stack.addWidget(page)
        hbox.addWidget(self.stack, stretch=1)

        # Conecta cada botón de la sidebar para cambiar de página
        for index, (name, _) in enumerate(items):
            btn = sidebar._btns[name]
            btn.clicked.connect(lambda _, i=index: self.stack.setCurrentIndex(i))

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
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())





