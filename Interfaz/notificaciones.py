from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class NotificacionesWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel('Vista: Notificaciones')
        layout.addWidget(label)
