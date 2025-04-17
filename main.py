from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Interfaz/home.ui", self)

        # Cargar los botones desde botonesHead.ui
        self.load_buttons()

    def load_buttons(self):
        # Cargar el diseño de botones desde botonesHead.ui
        botones_widget = QWidget()
        loadUi("Interfaz/botonesHead.ui", botones_widget)

        # Añadir el diseño de botones al layout principal
        central_layout = self.centralwidget.layout()
        central_layout.insertWidget(0, botones_widget)  # Insertar en la parte superior

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
