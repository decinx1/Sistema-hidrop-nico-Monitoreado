from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import random


class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Scroll principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Contenedor principal dentro del scroll
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(40)

        # Agregar secciones
        self.add_graphs_row(
            ("pH", [6.5, 6.8, 7.0, 6.9]),
            ("Temperatura (°C)", [20, 22, 23, 21])
        )

        self.add_graphs_row(
            ("CE (mS/cm)", [1.2, 1.3, 1.4, 1.5]),
            ("Nivel (cm)", [10, 12, 11, 13])
        )

        self.add_section_title("Escala Visual de pH")
        self.add_ph_scale()

        self.add_section_title("Medidor de pH Actual")
        self.add_ph_gauge(7.0)  # Inicialmente pH 7.0

        # Simulación cada 2 segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_ph_update)
        self.timer.start(2000)  # cada 2000 ms = 2 segundos

        # Finaliza el scroll
        scroll_area.setWidget(container)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

    def add_section_title(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        self.main_layout.addWidget(label)

    def add_graphs_row(self, graph1, graph2):
        row = QHBoxLayout()
        row.setSpacing(30)

        card1 = self.create_card(graph1[0], graph1[1])
        row.addWidget(card1)

        card2 = self.create_card(graph2[0], graph2[1])
        row.addWidget(card2)

        self.main_layout.addLayout(row)

    def create_card(self, title, data):
        frame = QFrame()
        frame.setMinimumHeight(350)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 15px;
                border: 1px solid #DDDDDD;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #34495e;
            }
        """)
        layout.addWidget(label)

        canvas = PlotCanvas(title, data)
        layout.addWidget(canvas)

        return frame

    def add_ph_scale(self):
        ph_card = QFrame()
        ph_card.setMinimumHeight(200)
        ph_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #DDDDDD;
            }
        """)
        layout = QVBoxLayout(ph_card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fig = Figure(figsize=(8, 2))
        ax = fig.add_subplot(111)

        ph_colors = [
            "#FF0000", "#FF4500", "#FF8C00", "#FFD700",
            "#ADFF2F", "#7CFC00", "#00FA9A", "#00CED1",
            "#1E90FF", "#4169E1", "#6A5ACD", "#8A2BE2",
            "#9400D3", "#8B008B"
        ]

        for idx, color in enumerate(ph_colors):
            ax.bar(idx, 1, color=color, edgecolor='none', width=1)

        ax.set_xlim(0, 14)
        ax.set_ylim(0, 1)
        ax.set_xticks([0, 7, 14])
        ax.set_xticklabels(["Ácido", "Neutral", "Alcalino"], fontsize=12, fontweight='bold')
        ax.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x', which='both', length=0)

        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.main_layout.addWidget(ph_card)

    def add_ph_gauge(self, ph_value):
        """Agrega velocímetro de pH y guarda el canvas."""
        self.gauge_card = QFrame()
        self.gauge_card.setMinimumHeight(400)
        self.gauge_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #DDDDDD;
            }
        """)
        self.gauge_layout = QVBoxLayout(self.gauge_card)
        self.gauge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ph_gauge_canvas = self.create_gauge_canvas(ph_value)
        self.gauge_layout.addWidget(self.ph_gauge_canvas)
        self.main_layout.addWidget(self.gauge_card)

    def create_gauge_canvas(self, ph_value):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 3))

        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_facecolor("white")

        ax.barh(1, np.pi/3, left=0, height=0.5, color="#ff4d4d")
        ax.barh(1, np.pi/3, left=np.pi/3, height=0.5, color="#f9e79f")
        ax.barh(1, np.pi/3, left=2*np.pi/3, height=0.5, color="#58d68d")

        theta = (ph_value / 14) * np.pi
        ax.plot([theta, theta], [0, 1], color='black', linewidth=3)

        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_ylim(0, 1)
        ax.spines['polar'].set_visible(False)
        ax.grid(False)

        fig.subplots_adjust(left=0.05, right=0.95, top=1.0, bottom=0)

        return FigureCanvas(fig)

    def simulate_ph_update(self):
        """Simula actualización de pH dinámicamente."""
        new_ph = round(random.uniform(5.5, 8.0), 2)
        self.update_ph_gauge(new_ph)

    def update_ph_gauge(self, ph_value):
        """Actualiza el medidor de pH."""
        # Quitar viejo canvas
        if self.ph_gauge_canvas:
            self.gauge_layout.removeWidget(self.ph_gauge_canvas)
            self.ph_gauge_canvas.setParent(None)

        # Agregar nuevo
        self.ph_gauge_canvas = self.create_gauge_canvas(ph_value)
        self.gauge_layout.addWidget(self.ph_gauge_canvas)


class PlotCanvas(FigureCanvas):
    def __init__(self, title, data, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.plot(title, data)

    def plot(self, title, data):
        self.axes.clear()

        x = np.linspace(1, len(data), len(data))
        y = np.array(data)

        xnew = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, y, k=2)
        y_smooth = spl(xnew)

        self.axes.plot(
            xnew, y_smooth,
            color='#3498db', linewidth=3,
            solid_capstyle='round'
        )
        self.axes.fill_between(xnew, y_smooth, color='#3498db', alpha=0.2)

        self.axes.scatter(
            x, y,
            color='#2ecc71', edgecolor='#27ae60', s=100, zorder=5
        )

        self.axes.set_facecolor('#ffffff')
        self.axes.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['left'].set_color('#cccccc')
        self.axes.spines['bottom'].set_color('#cccccc')

        self.axes.set_xlabel("Tiempo", fontsize=12, color='#34495e', labelpad=15)
        self.axes.set_ylabel("Valor", fontsize=12, color='#34495e', labelpad=15)
        self.axes.tick_params(axis='both', labelsize=10, colors='#34495e')

        self.draw()
