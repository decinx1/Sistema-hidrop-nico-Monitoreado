import sys
from PyQt6.QtWidgets import QApplication, QButtonGroup
from PyQt6.QtGui import QIcon  # Importa QIcon para manejar íconos
from PyQt6.uic import loadUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loadUi("home.ui")  # carga la interfaz de usuario desde el archivo .ui
    button_group = QButtonGroup(window)
    window.btnHome.setChecked(True)
    button_group.setExclusive(True)
    # Agregamos los botones al grupo
    button_group.addButton(window.btnHome)
    button_group.addButton(window.btnDatos)
    button_group.addButton(window.btnHistorial)
    window.setWindowTitle("HydroTech")  # establece el título de la ventana
    window.setWindowIcon(QIcon("Iconos/icono.ico"))  # Establece el icono de la ventana
    window.showMaximized()
    sys.exit(app.exec())
