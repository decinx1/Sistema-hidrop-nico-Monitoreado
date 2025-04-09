import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loadUi("home.ui")  # carga la interfaz de usuario desde el archivo .ui
    window.setWindowTitle("HydroTech")  # establece el título de la ventana
    #window.setWindowIcon(QIcon("icono.ico"))  # Establece el icono de la ventana
    window.showMaximized()
    sys.exit(app.exec())
