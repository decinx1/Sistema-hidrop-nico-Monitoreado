from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class UsuarioWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Vista: Usuario')
        layout.addWidget(label)
