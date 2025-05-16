from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import random
    

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración del scroll principal
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Contenedor principal
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(40)

        # Secciones de gráficos
        self.add_graphs_row(
            ("pH", [5.5, 6.8, 7.0, 6.9]),
            ("Temperatura (°C)", [30, 22, 23, 21]),
            ["Interfaz/icons/ph.png", "Interfaz/icons/temp.png"]
        )
        self.add_graphs_row(
            ("CE (mS/cm)", [1.2, 1.3, 1.4, 1.5]),
            ("Nivel (cm)", [10, 12, 11, 13]),
            ["Interfaz/icons/ce.png", "Interfaz/icons/nivel.png"]
        )

        # Secciones de pH
        self.add_section_title("Escala Visual de pH")
        self.add_ph_scale()
        self.add_section_title("Medidor de pH Actual")
        self.add_ph_gauge(7.0)

        # Temporizador para simulación
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_ph_update)
        self.timer.start(2000)

        # Configuración final del layout
        scroll_area.setWidget(container)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

    def add_section_title(self, text):
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ## Estilos para fuente de título de sección de medidor ph
        font = label.font()
        font.setPointSize(14)
        font.setFamily("Arial Rounded MT Bold")
        font.setBold(True)
        label.setFont(font)

        self.main_layout.addWidget(label)


    def add_graphs_row(self, graph1, graph2, icons):
        row = QHBoxLayout()
        row.setSpacing(30)

        row.addWidget(self.create_card_with_icons(graph1[0], graph1[1], icons[0]))
        row.addWidget(self.create_card_with_icons(graph2[0], graph2[1], icons[1]))
        self.main_layout.addLayout(row)

    def create_card_with_icons(self, title, data, icon_path):
        frame = QFrame()
        frame.setObjectName("cardFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Contenedor para íconos y título
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)

        # Ícono antes del título
        icon_before = QLabel()
        icon_before.setPixmap(QPixmap(icon_path))
        title_layout.addWidget(icon_before)

        # Título
        label = QLabel(title)
        label.setObjectName("graphTitle")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estilos para fuente de título de la gráfica
        font = label.font()
        font.setPointSize(14)
        font.setFamily("Arial Rounded MT Bold")
        font.setBold(True)
        label.setFont(font)
        title_layout.addWidget(label)

        # Ícono después del título
        icon_after = QLabel()
        icon_after.setPixmap(QPixmap("Interfaz/icons/info2.png"))
        title_layout.addWidget(icon_after)

        # Alinear el layout de título
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(title_layout)

        canvas = PlotCanvas(title, data)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.setMinimumHeight(300)
        layout.addWidget(canvas)
        return frame

    def add_ph_scale(self):
        ph_card = QFrame()
        ph_card.setObjectName("phScaleFrame")
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
        [ax.spines[side].set_visible(False) for side in ['top', 'right', 'left', 'bottom']]
        ax.tick_params(axis='x', which='both', length=0)

        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        layout.addWidget(FigureCanvas(fig))

        ph_canvas = FigureCanvas(fig)
        ph_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ph_canvas.setMinimumHeight(150)
        layout.addWidget(ph_canvas)

        self.main_layout.addWidget(ph_card)

    def add_ph_gauge(self, ph_value):
        self.gauge_card = QFrame()
        self.gauge_card.setObjectName("gaugeFrame")
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

        # Zonas de color
        ax.barh(1, np.pi/3, left=0, height=0.5, color="#ff4d4d")  # Ácido
        ax.barh(1, np.pi/3, left=np.pi/3, height=0.5, color="#f9e79f")  # Neutral
        ax.barh(1, np.pi/3, left=2*np.pi/3, height=0.5, color="#58d68d")  # Alcalino

        # Aguja
        theta = (ph_value / 14) * np.pi
        ax.plot([theta, theta], [0, 1], color='black', linewidth=3)

        # Configuración visual
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_ylim(0, 1)
        ax.spines['polar'].set_visible(False)
        ax.grid(False)
        fig.subplots_adjust(left=0.05, right=0.95, top=1.0, bottom=0)

        gauge_canvas = FigureCanvas(fig)
        gauge_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        gauge_canvas.setMinimumHeight(200)

        return gauge_canvas

    def simulate_ph_update(self):
        new_ph = round(random.uniform(5.5, 8.0), 2)
        self.update_ph_gauge(new_ph)

    def update_ph_gauge(self, ph_value):
        if self.ph_gauge_canvas:
            self.gauge_layout.removeWidget(self.ph_gauge_canvas)
            self.ph_gauge_canvas.setParent(None)
        
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
        
        # Suavizado de curva
        xnew = np.linspace(x.min(), x.max(), 300)
        spl = make_interp_spline(x, y, k=2)
        y_smooth = spl(xnew)

        # Gráfico principal
        self.axes.plot(xnew, y_smooth, color='#3498db', linewidth=3, solid_capstyle='round')

        # Estilos del gráfico 
        self.axes.set_facecolor('#ffffff')
        self.axes.grid(True, linestyle='--', linewidth= 0.5, alpha= 0.6, color = '#0000FF')
        [self.axes.spines[side].set_visible(False) for side in ['top', 'right']]
        self.axes.spines['left'].set_color('#cccccc')
        self.axes.spines['bottom'].set_color('#cccccc')
        self.axes.set_xlabel("Tiempo", fontsize=12, color='#34495e', labelpad=15)
        self.axes.set_ylabel("Valor", fontsize=12, color='#34495e', labelpad=15)
        self.axes.tick_params(axis='both', labelsize=10, colors='#34495e')

        # colorear segun rango de valores
        if title.lower().startswith("ph"):
            #Se colorea segun el rango que se establezca
            self.axes.axhspan(0, 5.5, facecolor="#FF0000", alpha=0.4) #Peligro ácido
            self.axes.axhspan(5.5, 6.0, facecolor="#f1c40f", alpha=0.4) #Advertencia ácido
            self.axes.axhspan(6.0, 6.8, facecolor="#00C853", alpha=0.4) #Óptimo
            self.axes.axhspan(6.8, 7.5, facecolor="#f1c40f", alpha=0.4) #Advertencia alcalino
            self.axes.axhspan(7.5, 14, facecolor="#FF0000", alpha=0.4) #Peligro alcalino
        elif "temperatura" in title.lower():
            self.axes.axhspan(0, 10, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(10, 18, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(18, 24, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(24, 30, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(30, 50, facecolor="#FF0000", alpha=0.4)
        elif "ce" in title.lower():
            self.axes.axhspan(0, 1, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(1, 1.5, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(1.5, 2.0, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(2.0, 2.5, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(2.5, 5, facecolor="#FF0000", alpha=0.4)
        elif "nivel" in title.lower():
            self.axes.axhspan(0, 10, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(10, 15, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(15, 25, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(25, 30, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(30, 35, facecolor="#FF0000", alpha=0.4)

        # Delimitacion de rangos
        if title.lower().startswith("ph"):
            self.axes.set_ylim(0, 14)  #Rango de PH 0-14
        elif "temperatura" in title.lower():
            self.axes.set_ylim(0, 40)  #Rango de temperatura 0-40
        elif "ce" in title.lower():
            self.axes.set_ylim(0, 4)
        elif "nivel" in title.lower():
            self.axes.set_ylim(0, 35)

        self.draw()