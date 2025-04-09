import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loadUi("home.ui")  # Carga el archivo home.ui
    window.show()
    sys.exit(app.exec())
