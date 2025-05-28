from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QSizePolicy, QToolTip
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
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


class DataFetchWorker(QObject):
    data_ready = pyqtSignal(dict)
    def __init__(self, obtener_datos_por_fecha):
        super().__init__()
        self.obtener_datos_por_fecha = obtener_datos_por_fecha
        self._running = True

    def stop(self):
        self._running = False

    def fetch_latest(self):
        # Llama a la base de datos y emite los datos
        datos = {'ph': [], 'temperatura': [], 'ce': [], 'nivel': []}
        if self.obtener_datos_por_fecha:
            from datetime import datetime
            hoy = datetime.now().strftime('%Y-%m-%d')
            try:
                registros = self.obtener_datos_por_fecha(hoy)
            except Exception:
                registros = None
            if registros:
                for sensor in datos.keys():
                    valores = [float(r[2]) for r in registros if r[1].lower() == sensor]
                    datos[sensor] = valores[-20:] if valores else []
        self.data_ready.emit(datos)

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
        if not self.simulando:
            self.series = self.inicializar_series()
        else:
            self.series = {'ph': [], 'temperatura': [], 'ce': [], 'nivel': []}

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
        ph_value = self.series['ph'][-1] if self.series['ph'] else 7.0  # Valor neutro si no hay datos
        self.add_ph_gauge(ph_value)

        # --- NUEVO: Hilo para consultas a la BD ---
        self.worker_thread = None
        self.worker = None
        if obtener_datos_por_fecha:
            self.worker_thread = QThread()
            self.worker = DataFetchWorker(obtener_datos_por_fecha)
            self.worker.moveToThread(self.worker_thread)
            self.worker.data_ready.connect(self.on_data_ready)
            self.worker_thread.start()
        # ---

        # --- Un solo temporizador para actualizar todo ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.solicitar_actualizacion_datos)
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
        # Si ph_value es None, usa 7.0
        if ph_value is None:
            ph_value = 7.0
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

        # --- BUCLE FOR AÑADIDO ---
        # Iteramos sobre cada llave ('ph', 'temperatura', 'ce', 'nivel')
        for k in datos.keys():
            # --- CÓDIGO DE RELLENO (DENTRO DEL BUCLE) ---
            if not datos[k]:
                # Si la lista está VACÍA, rellénala con 20 ceros
                datos[k] = [0] * 20
            elif len(datos[k]) < 20:
                # Si NO está vacía PERO es más corta de 20, rellénala con su primer elemento
                datos[k] = [datos[k][0]] * (20 - len(datos[k])) + datos[k]
            # --- FIN CÓDIGO DE RELLENO ---

        return datos

    def actualizar_en_tiempo_real(self):
        # Simula/agrega solo el último dato (o real si hay BD)
        nuevo = self.obtener_nuevo_dato()
        for k in self.series:
            self.series[k].append(nuevo[k])
            if len(self.series[k]) > 20:
                self.series[k].pop(0)
        # Evita error si no hay datos válidos
        ph_value = self.series['ph'][-1] if self.series['ph'] and self.series['ph'][-1] is not None else 7.0
        self.actualizar_graficas_en_tiempo_real()
        self.update_ph_gauge(ph_value)

    def closeEvent(self, event):
        # Detener el hilo de la base de datos al cerrar
        if hasattr(self, 'worker_thread') and self.worker_thread is not None:
            if hasattr(self, 'worker') and self.worker is not None:
                try:
                    self.worker.stop()
                except Exception:
                    pass
            try:
                self.worker_thread.quit()
                self.worker_thread.wait(2000)  # Espera hasta 2 segundos
            except Exception:
                pass
            self.worker_thread = None
            self.worker = None
        super().closeEvent(event)

    def solicitar_actualizacion_datos(self):
        # Llama al worker en el hilo secundario
        if self.worker:
            QTimer.singleShot(0, self.worker.fetch_latest)
        else:
            self.actualizar_en_tiempo_real()  # fallback si no hay worker

    def on_data_ready(self, datos):
        # Actualiza las series y la UI con los datos recibidos del hilo
        for k in datos:
            if k in self.series:
                self.series[k].append(datos[k][-1] if datos[k] else None)
                if len(self.series[k]) > 20:
                    self.series[k].pop(0)
        ph_value = self.series['ph'][-1] if self.series['ph'] and self.series['ph'][-1] is not None else 7.0
        self.actualizar_graficas_en_tiempo_real()
        self.update_ph_gauge(ph_value)

    def obtener_datos_recientes(self):
        # Obtiene los datos de la última hora (solo reales, sin simulación)
        datos = {'ph': [], 'temperatura': [], 'ce': [], 'nivel': []}
        if obtener_datos_por_fecha:
            hoy = datetime.now().strftime('%Y-%m-%d')
            registros = obtener_datos_por_fecha(hoy)
            if registros:
                for sensor in datos.keys():
                    valores = [float(r[2]) for r in registros if r[1].lower() == sensor]
                    datos[sensor] = valores[-20:] if valores else []
        return datos

    def obtener_nuevo_dato(self):
        # Solo datos reales, sin simulación
        if obtener_datos_por_fecha:
            hoy = datetime.now().strftime('%Y-%m-%d')
            registros = obtener_datos_por_fecha(hoy)
            if registros:
                nuevo = {}
                for sensor in self.series.keys():
                    valores = [float(r[2]) for r in registros if r[1].lower() == sensor]
                    nuevo[sensor] = valores[-1] if valores else None
                return nuevo
        return {k: None for k in self.series.keys()}

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
        # Obtiene los datos de la última hora (solo reales, sin simulación)
        datos = {'ph': [], 'temperatura': [], 'ce': [], 'nivel': []}
        if obtener_datos_por_fecha:
            hoy = datetime.now().strftime('%Y-%m-%d')
            registros = obtener_datos_por_fecha(hoy)
            if registros:
                for sensor in datos.keys():
                    valores = [float(r[2]) for r in registros if r[1].lower() == sensor]
                    datos[sensor] = valores[-20:] if valores else []
        return datos


class PlotCanvas(FigureCanvas):
    def __init__(self, title, data, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.plot(title, data)

    def plot(self, title, data):
        self.axes.clear()
        # --- MODERNIZA ESTILO DE LA GRÁFICA ---
        self.figure.set_facecolor('#e8ecf3')  # gris-azulado suave
        self.axes.set_facecolor('#f5f7fa')  # blanco azulado
        axis_color = '#6a8caf'
        self.axes.spines['left'].set_color(axis_color)
        self.axes.spines['bottom'].set_color(axis_color)
        self.axes.spines['left'].set_linewidth(2)
        self.axes.spines['bottom'].set_linewidth(2)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.tick_params(axis='both', labelsize=11, colors=axis_color, width=1.5)
        self.axes.grid(True, linestyle='--', linewidth=1, alpha=0.18, color='#34495e')
        self.axes.set_xlabel("Tiempo", fontsize=13, color=axis_color, labelpad=15, fontweight='bold')
        # --- FIN MODERNIZA ESTILO ---

        # Filtrar datos inválidos (None, nan, inf) para evitar crash en interpolación
        if data:
            x = np.arange(len(data))
            y = np.array(data, dtype=float)
            mask = np.isfinite(y)
            x = x[mask]
            y = y[mask]
        else:
            x = np.array([])
            y = np.array([])
        # --- CORRECCIÓN: solo interpola si hay al menos 2 puntos ---
        if len(x) >= 2:
            xnew = np.linspace(x.min(), x.max(), 300)
            spl = make_interp_spline(x, y, k=2)
            y_smooth = spl(xnew)
            self.axes.plot(xnew, y_smooth, color='#3498db', linewidth=3, solid_capstyle='round', zorder=3)
        elif len(x) == 1:
            self.axes.plot(x, y, 'o', color='#3498db', markersize=8, zorder=3)
        if len(x) > 1:
            minutos = 8
            labels = [f"-{(len(x)-i-1)*minutos}min" for i in range(len(x))]
            step = max(1, len(x)//6)
            self.axes.set_xticks(x[::step])
            self.axes.set_xticklabels(labels[::step], rotation=30, fontsize=10, color=axis_color)
        # Coloreado de rangos: rojo (peligro), amarillo (advertencia), verde (ok)
        if title.lower().startswith("ph"):
            self.axes.axhspan(0, 5.5, facecolor="#FF0000", alpha=0.4)      # rojo
            self.axes.axhspan(5.5, 6.0, facecolor="#f1c40f", alpha=0.4)    # amarillo
            self.axes.axhspan(6.0, 6.8, facecolor="#00C853", alpha=0.4)    # verde
            self.axes.axhspan(6.8, 7.5, facecolor="#f1c40f", alpha=0.4)    # amarillo
            self.axes.axhspan(7.5, 14, facecolor="#FF0000", alpha=0.4)     # rojo
            self.axes.set_ylim(0, 14)
        elif "temperatura" in title.lower():
            self.axes.axhspan(0, 10, facecolor="#FF0000", alpha=0.4)       # rojo
            self.axes.axhspan(10, 4, facecolor="#f1c40f", alpha=0.4)      # amarillo
            self.axes.axhspan(4, 24, facecolor="#00C853", alpha=0.4)      # verde
            self.axes.axhspan(24, 30, facecolor="#f1c40f", alpha=0.4)      # amarillo
            self.axes.axhspan(30, 50, facecolor="#FF0000", alpha=0.4)      # rojo
            self.axes.set_ylim(0, 40)
        elif "ce" in title.lower():
            self.axes.axhspan(0, 1, facecolor="#FF0000", alpha=0.4)        # rojo
            self.axes.axhspan(1, 1.5, facecolor="#f1c40f", alpha=0.4)      # amarillo
            self.axes.axhspan(1.5, 2.0, facecolor="#00C853", alpha=0.4)    # verde
            self.axes.axhspan(2.0, 2.5, facecolor="#f1c40f", alpha=0.4)    # amarillo
            self.axes.axhspan(2.5, 5, facecolor="#FF0000", alpha=0.4)      # rojo
            self.axes.set_ylim(0, 4)
        elif "nivel" in title.lower():
            self.axes.axhspan(0, 10, facecolor="#FF0000", alpha=0.4)       # rojo
            self.axes.axhspan(10, 15, facecolor="#f1c40f", alpha=0.4)      # amarillo
            self.axes.axhspan(15, 25, facecolor="#00C853", alpha=0.4)      # verde
            self.axes.axhspan(25, 30, facecolor="#f1c40f", alpha=0.4)      # amarillo
            self.axes.axhspan(30, 35, facecolor="#FF0000", alpha=0.4)      # rojo
            self.axes.set_ylim(0, 35)
        self.draw()
