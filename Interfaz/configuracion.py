from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.uic import loadUi
import os

class ConfiguracionWindow(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ui', 'configuracion.ui')
        loadUi(ui_path, self)
