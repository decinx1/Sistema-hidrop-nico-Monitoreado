from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from PyQt6.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class HomeWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        loadUi("Interfaz/home.ui", self)
        self.setup_graphics()

    def setup_graphics(self):
        self.add_graph_to_widget(self.pH_Grafico, "pH", [6.5, 6.8, 7.0, 6.9])
        self.add_graph_to_widget(self.temp_Grafica, "Temperatura (°C)", [20, 22, 23, 21])
        self.add_graph_to_widget(self.CE_Grafica, "CE (mS/cm)", [1.2, 1.3, 1.4, 1.5])
        self.add_graph_to_widget(self.ultrasonico_Grafica, "Nivel (cm)", [10, 12, 11, 13])

    def add_graph_to_widget(self, widget, title, data):
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
        x = range(1, len(data) + 1)  # Generar valores para el eje X
        self.axes.plot(
            x, data, 
            marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8, 
            markerfacecolor='orange', markeredgecolor='black'
        )
        self.axes.set_title(title, fontsize=14, fontweight='bold', color='#333333')
        self.axes.set_xlabel("Tiempo", fontsize=12, fontweight='bold', color='#555555')
        self.axes.set_ylabel("Valor", fontsize=12, fontweight='bold', color='#555555')
        self.axes.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        self.axes.set_facecolor('#f9f9f9')  # Fondo de la gráfica
        self.axes.spines['top'].set_visible(False)  # Ocultar borde superior
        self.axes.spines['right'].set_visible(False)  # Ocultar borde derecho
        self.axes.tick_params(axis='both', which='major', labelsize=10, colors='#555555')
        self.draw()