from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QComboBox, QPushButton
from PyQt6.uic import loadUi
import os

class ConfiguracionWindow(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ui', 'configuracion.ui')
        loadUi(ui_path, self)
        self.btnGuardar.clicked.connect(self.cambiar_resolucion)
        # Botón: Información del sistema
        self.btnInfo = QPushButton("Información del sistema", self)
        self.btnInfo.setStyleSheet("font-size:15px; margin-top:8px; background:#607d8b; color:white; border-radius:8px; padding:8px 0;")
        self.verticalLayout.addWidget(self.btnInfo)
        self.btnInfo.clicked.connect(self.mostrar_info)
        # Soporte
        self.btnSoporte = QPushButton("Soporte / Contacto", self)
        self.btnSoporte.setStyleSheet("font-size:15px; margin-top:8px; background:#1976D2; color:white; border-radius:8px; padding:8px 0;")
        self.verticalLayout.addWidget(self.btnSoporte)
        self.btnSoporte.clicked.connect(self.mostrar_soporte)

    def mostrar_info(self):
        QMessageBox.information(self, "Información del sistema", "<b>Versión:</b> 1.0.0<br><b>Autores:</b> <br>Aguilar Gustavo Salvador<br>Alaniz Munguia Luis <br> Carmona Cernas Flor <br>Gonzalez Gonzalez Alan <br> Larios Rosas Victor <br> Rivera Meza Jesus<br>")

    def cambiar_resolucion(self):
        resol = self.comboResolucion.currentText()
        try:
            w, h = map(int, resol.split('x'))
            main_win = self.window()
            from PyQt6.QtGui import QGuiApplication
            screen = QGuiApplication.primaryScreen()
            screen_size = screen.size()
            if w == screen_size.width() and h == screen_size.height():
                main_win.showFullScreen()
            else:
                main_win.showNormal()
                main_win.resize(w, h)
            QMessageBox.information(self, "Resolución", f"Resolución cambiada a {w}x{h}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo cambiar la resolución: {e}")

    def mostrar_soporte(self):
        QMessageBox.information(self, "Soporte / Contacto", "¿Necesitas ayuda?\n\nEmail: soporte@hidroponia.com\nWhatsApp: +52 123 456 7890\nSitio web: www.hidroponia.com/soporte")
