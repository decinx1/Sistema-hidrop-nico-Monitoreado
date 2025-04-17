import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class GraficaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráficas Simuladas")
        self.setGeometry(100, 100, 800, 600)

        # Crear un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear un layout vertical
        layout = QVBoxLayout(central_widget)

        # Crear una figura de matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Generar una gráfica simulada
        self.plot_simulada()

    def plot_simulada(self):
        ax = self.figure.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)  # Datos simulados
        ax.plot(x, y, label="Simulación")
        ax.set_title("Gráfica Simulada")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Valor")
        ax.legend()
        self.canvas.draw()

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("home.ui", self)  # Carga el archivo .ui

        # Configurar gráficas en los widgets
        self.setup_graphics()

    def setup_graphics(self):
        # Crear y asignar gráficas a los widgets
        self.add_graph_to_widget(self.pH_Grafico, "pH", [6.5, 6.8, 7.0, 6.9])
        self.add_graph_to_widget(self.temp_Grafica, "Temperatura (°C)", [20, 22, 23, 21])
        self.add_graph_to_widget(self.CE_Grafica, "CE (mS/cm)", [1.2, 1.3, 1.4, 1.5])
        self.add_graph_to_widget(self.ultrasonico_Grafica, "Nivel (cm)", [10, 12, 11, 13])

    def add_graph_to_widget(self, widget, title, data):
        # Crear un contenedor para la gráfica
        layout = QVBoxLayout(widget)
        canvas = PlotCanvas(title, data)
        layout.addWidget(canvas)
        widget.setLayout(layout)

class PlotCanvas(FigureCanvas):
    def __init__(self, title, data, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.plot(title, data)

    def plot(self, title, data):
        self.axes.clear()
        self.axes.plot(data, marker='o', linestyle='-', color='b')
        self.axes.set_title(title)
        self.axes.grid(True)
        self.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = HomeWindow()
    main_window.showMaximized()
    sys.exit(app.exec())
