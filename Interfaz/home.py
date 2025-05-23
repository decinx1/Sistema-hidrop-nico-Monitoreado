from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QSizePolicy, QToolTip
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

# Importa la función para obtener datos recientes de la BD
try:
    from Interfaz.conexion_cliente import obtener_datos_por_fecha
except ImportError:
    obtener_datos_por_fecha = None


class HoverLabel(QLabel):
    def __init__(self, tooltip_text="", parent=None):
        super().__init__(parent)
        self.tooltip_text = tooltip_text

    def enterEvent(self, event):
        QToolTip.showText(self.mapToGlobal(self.rect().center()), self.tooltip_text, self)
        super().enterEvent(event)


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

        # --- NUEVO: Cargar datos reales o simular si no hay conexión ---
        self.datos_recientes = self.obtener_datos_recientes()
        # Guardar si estamos simulando o usando BD
        self.simulando = not any(self.datos_recientes.values()) or not obtener_datos_por_fecha
        # ---

        # --- NUEVO: Inicializa series en memoria (FIFO) ---
        self.series = self.inicializar_series()

        # Secciones de gráficos con tooltips personalizados
        self.add_graphs_row(
            ("pH", self.series['ph']),
            ("Temperatura (°C)", self.series['temperatura']),
            ["Interfaz/icons/ph.png", "Interfaz/icons/temp.png"],
            [
                "El pH mide la acidez o alcalinidad de la solución nutritiva.",
                "La temperatura afecta la absorción de nutrientes por las raíces."
            ]
        )
        self.add_graphs_row(
            ("CE (mS/cm)", self.series['ce']),
            ("Nivel (cm)", self.series['nivel']),
            ["Interfaz/icons/ce.png", "Interfaz/icons/nivel.png"],
            [
                "La CE indica la concentración de sales disueltas en el agua.",
                "El nivel de agua debe ser estable para evitar estrés hídrico."
            ]
        )

        # Sección del medidor de pH
        self.add_section_title("Medidor de pH Actual")
        self.add_ph_gauge(self.series['ph'][-1])

        # --- Un solo temporizador para actualizar todo ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_en_tiempo_real)
        self.timer.start(8000)  # Cada 8 segundos

        # Configuración final del layout
        scroll_area.setWidget(container)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

    def add_section_title(self, text):
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setPointSize(14)
        font.setFamily("Arial Rounded MT Bold")
        font.setBold(True)
        label.setFont(font)
        self.main_layout.addWidget(label)

    def add_graphs_row(self, graph1, graph2, icons, tooltips):
        row = QHBoxLayout()
        row.setSpacing(30)
        row.addWidget(self.create_card_with_icons(graph1[0], graph1[1], icons[0], tooltips[0]))
        row.addWidget(self.create_card_with_icons(graph2[0], graph2[1], icons[1], tooltips[1]))
        self.main_layout.addLayout(row)

    def create_card_with_icons(self, title, data, icon_path, tooltip_text):
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
        font = label.font()
        font.setPointSize(14)
        font.setFamily("Arial Rounded MT Bold")
        font.setBold(True)
        label.setFont(font)
        title_layout.addWidget(label)

        # Ícono después del título con tooltip personalizado
        icon_after = HoverLabel(tooltip_text)
        icon_after.setPixmap(QPixmap("Interfaz/icons/info2.png"))
        icon_after.setCursor(Qt.CursorShape.PointingHandCursor)
        title_layout.addWidget(icon_after)

        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(title_layout)

        canvas = PlotCanvas(title, data)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.setMinimumHeight(300)
        layout.addWidget(canvas)
        return frame

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

    def update_ph_gauge(self, ph_value):
        if self.ph_gauge_canvas:
            self.gauge_layout.removeWidget(self.ph_gauge_canvas)
            self.ph_gauge_canvas.setParent(None)
        self.ph_gauge_canvas = self.create_gauge_canvas(ph_value)
        self.gauge_layout.addWidget(self.ph_gauge_canvas)

    def inicializar_series(self):
        # Obtiene los datos iniciales (BD o simulados)
        datos = self.obtener_datos_recientes()
        # Asegura longitud 20
        for k in datos:
            if len(datos[k]) < 20:
                datos[k] = [datos[k][0]] * (20 - len(datos[k])) + datos[k]
            else:
                datos[k] = datos[k][-20:]
        return datos

    def actualizar_en_tiempo_real(self):
        # Simula/agrega solo el último dato (o real si hay BD)
        nuevo = self.obtener_nuevo_dato()
        for k in self.series:
            self.series[k].append(nuevo[k])
            if len(self.series[k]) > 20:
                self.series[k].pop(0)
        self.actualizar_graficas_en_tiempo_real()
        self.update_ph_gauge(self.series['ph'][-1])

    def obtener_nuevo_dato(self):
        # Si hay BD, trae solo el último dato; si no, simula
        if obtener_datos_por_fecha:
            hoy = datetime.now().strftime('%Y-%m-%d')
            registros = obtener_datos_por_fecha(hoy)
            if registros:
                nuevo = {}
                for sensor in self.series.keys():
                    valores = [float(r[2]) for r in registros if r[1].lower() == sensor]
                    nuevo[sensor] = valores[-1] if valores else self.series[sensor][-1]
                return nuevo
        # Simulación
        return {
            'ph': round(random.uniform(5.8, 7.2), 2),
            'temperatura': round(random.uniform(20, 25), 1),
            'ce': round(random.uniform(1.1, 1.6), 2),
            'nivel': round(random.uniform(10, 14), 1),
        }

    def actualizar_graficas_en_tiempo_real(self):
        # Actualiza las gráficas de la ventana Home
        filas = [self.main_layout.itemAt(i) for i in range(self.main_layout.count()) if isinstance(self.main_layout.itemAt(i), QHBoxLayout)]
        if len(filas) >= 2:
            # Primera fila: pH y Temperatura
            row1 = self.main_layout.itemAt(0).layout()
            if row1:
                card_ph = row1.itemAt(0).widget()
                card_temp = row1.itemAt(1).widget()
                self._actualizar_card_grafica(card_ph, 'pH', self.series['ph'])
                self._actualizar_card_grafica(card_temp, 'Temperatura (°C)', self.series['temperatura'])
            # Segunda fila: CE y Nivel
            row2 = self.main_layout.itemAt(1).layout()
            if row2:
                card_ce = row2.itemAt(0).widget()
                card_nivel = row2.itemAt(1).widget()
                self._actualizar_card_grafica(card_ce, 'CE (mS/cm)', self.series['ce'])
                self._actualizar_card_grafica(card_nivel, 'Nivel (cm)', self.series['nivel'])

    def _actualizar_card_grafica(self, card, titulo, datos):
        # Busca el PlotCanvas dentro del card y actualiza la gráfica
        for i in range(card.layout().count()):
            widget = card.layout().itemAt(i).widget()
            if isinstance(widget, PlotCanvas):
                widget.plot(titulo, datos)
                break

    def obtener_datos_recientes(self):
        # Obtiene los datos de la última hora (o simula si no hay BD)
        datos = {'ph': [], 'temperatura': [], 'ce': [], 'nivel': []}
        if obtener_datos_por_fecha:
            hoy = datetime.now().strftime('%Y-%m-%d')
            registros = obtener_datos_por_fecha(hoy)
            if registros:
                for sensor in datos.keys():
                    valores = [float(r[2]) for r in registros if r[1].lower() == sensor]
                    datos[sensor] = valores[-20:] if valores else [0]
        # Si no hay datos, simula
        if not any(datos.values()) or not obtener_datos_por_fecha:
            datos = {
                'ph': [round(random.uniform(5.8, 7.2), 2) for _ in range(20)],
                'temperatura': [round(random.uniform(20, 25), 1) for _ in range(20)],
                'ce': [round(random.uniform(1.1, 1.6), 2) for _ in range(20)],
                'nivel': [round(random.uniform(10, 14), 1) for _ in range(20)],
            }
        return datos


class PlotCanvas(FigureCanvas):
    def __init__(self, title, data, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.plot(title, data)

    def plot(self, title, data):
        self.axes.clear()
        x = np.arange(len(data))
        y = np.array(data)
        if len(x) > 1:
            xnew = np.linspace(x.min(), x.max(), 300)
            spl = make_interp_spline(x, y, k=2)
            y_smooth = spl(xnew)
        else:
            xnew, y_smooth = x, y
        self.axes.plot(xnew, y_smooth, color='#3498db', linewidth=3, solid_capstyle='round')
        self.axes.set_facecolor('#ffffff')
        self.axes.grid(True, linestyle='--', linewidth=0.5, alpha=0.6, color='#0000FF')
        [self.axes.spines[side].set_visible(False) for side in ['top', 'right']]
        self.axes.spines['left'].set_color('#cccccc')
        self.axes.spines['bottom'].set_color('#cccccc')
        # Eje X: muestra tiempo relativo si hay suficientes datos
        if len(x) > 1:
            minutos = 8
            labels = [f"-{(len(x)-i-1)*minutos}min" for i in range(len(x))]
            step = max(1, len(x)//6)
            self.axes.set_xticks(x[::step])
            self.axes.set_xticklabels(labels[::step], rotation=30, fontsize=9)
        self.axes.set_xlabel("Tiempo", fontsize=12, color='#34495e', labelpad=15)
        self.axes.set_ylabel("Valor", fontsize=12, color='#34495e', labelpad=15)
        self.axes.tick_params(axis='both', labelsize=10, colors='#34495e')

        if title.lower().startswith("ph"):
            self.axes.axhspan(0, 5.5, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(5.5, 6.0, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(6.0, 6.8, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(6.8, 7.5, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(7.5, 14, facecolor="#FF0000", alpha=0.4)
            self.axes.set_ylim(0, 14)
        elif "temperatura" in title.lower():
            self.axes.axhspan(0, 10, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(10, 18, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(18, 24, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(24, 30, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(30, 50, facecolor="#FF0000", alpha=0.4)
            self.axes.set_ylim(0, 40)
        elif "ce" in title.lower():
            self.axes.axhspan(0, 1, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(1, 1.5, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(1.5, 2.0, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(2.0, 2.5, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(2.5, 5, facecolor="#FF0000", alpha=0.4)
            self.axes.set_ylim(0, 4)
        elif "nivel" in title.lower():
            self.axes.axhspan(0, 10, facecolor="#FF0000", alpha=0.4)
            self.axes.axhspan(10, 15, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(15, 25, facecolor="#00C853", alpha=0.4)
            self.axes.axhspan(25, 30, facecolor="#f1c40f", alpha=0.4)
            self.axes.axhspan(30, 35, facecolor="#FF0000", alpha=0.4)
            self.axes.set_ylim(0, 35)

        self.draw()
