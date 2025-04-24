from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from Interfaz.datos import DatosView  # Importar la clase DatosView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear widget central con layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Crear la vista de datos
        self.datos_view = DatosView()
        layout.addWidget(self.datos_view)

        # Establecer como widget central
        self.setCentralWidget(central_widget)
        self.setWindowTitle("HydroTech")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()