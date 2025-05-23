from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ConfiguracionWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Vista: Configuración')
        layout.addWidget(label)
