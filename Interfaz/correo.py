from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CorreoWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Vista: Correo')
        layout.addWidget(label)
