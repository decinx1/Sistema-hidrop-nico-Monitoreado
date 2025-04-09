import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon  # Importa QIcon para manejar íconos
from PyQt6.uic import loadUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loadUi("calendar.ui")  # Carga la interfaz de usuario desde el archivo .ui
    window.setWindowTitle("HydroTech")  # Establece el título de la ventana
    window.setWindowIcon(QIcon("Iconos/icono.ico"))  # Establece el ícono de la ventana
    window.showMaximized()
    sys.exit(app.exec())
