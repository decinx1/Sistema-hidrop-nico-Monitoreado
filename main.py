from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QButtonGroup
from PyQt6.uic import loadUi
from Interfaz.home import HomeWindow  # Asegúrate de que el path sea correcto

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear widget central con layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Cargar botones (parte superior)
        botones_widget = QWidget()
        loadUi("Interfaz/botonesHead.ui", botones_widget)
        layout.addWidget(botones_widget)

        # Crear un grupo de botones para que sean mutuamente excluyentes
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(botones_widget.findChild(QWidget, "btnHome"))
        self.button_group.addButton(botones_widget.findChild(QWidget, "btnDatos"))
        self.button_group.addButton(botones_widget.findChild(QWidget, "btnHistorial"))

        # Seleccionar el botón "Home" por defecto
        btn_home = botones_widget.findChild(QWidget, "btnHome")
        btn_home.setChecked(True)

        # Cargar vista de gráficas (parte inferior)
        home_view = HomeWindow()
        layout.addWidget(home_view)

        # Establecer como widget central
        self.setCentralWidget(central_widget)
        self.setWindowTitle("HydroTech")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()