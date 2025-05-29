from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QHeaderView, QLabel,
    QVBoxLayout, QDialog, QGraphicsOpacityEffect,
    QStyledItemDelegate, QFrame, QSizePolicy, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor, QPen, QBrush, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF, QSize
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

# Ruta robusta del icono
icon_path = os.path.join(os.path.dirname(__file__), "icons", "menu.png")

class CenteredIconDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        icon = index.data(Qt.ItemDataRole.DecorationRole)
        if isinstance(icon, QIcon):
            size = QSize(32, 32)
            pixmap = icon.pixmap(size)
            x = option.rect.x() + (option.rect.width() - size.width()) // 2
            y = option.rect.y() + (option.rect.height() - size.height()) // 2
            painter.drawPixmap(x, y, pixmap)
        else:
            super().paint(painter, option, index)

class RoundedTextDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()

        text = index.data(Qt.ItemDataRole.DisplayRole)
        if not text:
            super().paint(painter, option, index)
            painter.restore()
            return

        rect = QRectF(option.rect.adjusted(8, 8, -8, -8))
        bg_color = QColor("#444")
        text_color = QColor("white")

        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 12, 12)

        painter.setPen(QPen(text_color))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.restore()

class DatosView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.resize(800, 600)

        # Central widget y layout principal
        central_widget = QFrame(self)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(central_widget)

        # Content widget y layout horizontal
        content_widget = QFrame(central_widget)
        content_layout = QHBoxLayout(content_widget)
        main_layout.addWidget(content_widget)

        # Tabla widget y layout horizontal (spacing 0)
        tabla_widget = QFrame(content_widget)
        tabla_layout = QHBoxLayout(tabla_widget)
        tabla_layout.setSpacing(0)
        content_layout.addWidget(tabla_widget)

        # QTableView
        self.table = QTableView(tabla_widget)
        tabla_layout.addWidget(self.table)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Nombre", "Datos", "Detalles"])

        data = [
            ["PH", "Indica si el agua es ácida, neutra o alcanila. un pH correcto ayuda a la absorción de nutrientes."],
            ["Nutrientes", "Son las sustancias disueltas en el agua que las plantas necesitan para crecer, como nitrógeno, fósforo y potasio."],
            ["Flujo del agua", "Es el movimiento del agua a través del sistema de riego, asegurando que las plantas reciban la cantidad adecuada."],
            ["Nivel del agua", "El volumen de agua disponible en el sistema, importante para mantener la salud de las plantas."],
        ]

        for row_data in data:
            items = [QStandardItem(cell) for cell in row_data]
            for item in items:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Deshabilitar edición
            icon_item = QStandardItem()
            icon_item.setIcon(QIcon(icon_path))
            icon_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_item.setFlags(icon_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Deshabilitar edición

            items.append(icon_item)
            self.model.appendRow(items)

        self.table.setModel(self.model)
        self.table.setIconSize(QSize(32, 32))

        delegate = RoundedTextDelegate()
        self.table.setItemDelegateForColumn(0, delegate)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)

        self.table.clicked.connect(self.on_table_click)

        # Agregar la escala visual de pH debajo de la tabla
        ph_label = QLabel("Escala de pH")
        ph_label.setObjectName("sectionTitle")
        main_layout.addWidget(ph_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ph_card = QFrame()
        self.add_ph_scale()
        main_layout.addWidget(self.ph_card)

    def show_details_modal(self, nombre, texto_detalle):
        modal = QDialog(self)
        modal.setWindowTitle("Detalles")
        modal.setFixedSize(420, 320)
        modal.setWindowModality(Qt.WindowModality.ApplicationModal)
        modal.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2=1, stop:0 #f5f7fa, stop:1 #c3cfe2);
                border: 2px solid #6a8caf;
                box-shadow: 0px 8px 32px rgba(60, 60, 100, 0.18);
            }
        """)

        layout = QVBoxLayout(modal)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # Título estilizado
        title = QLabel(nombre)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2a3b4c;
                letter-spacing: 1px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Línea decorativa
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background: #6a8caf; min-height:2px; max-height:2px; border:none;")
        layout.addWidget(line)

        # Texto de detalles
        details_label = QLabel(texto_detalle)
        details_label.setWordWrap(True)
        details_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #223344;
                padding: 8px 0 8px 0;
                line-height: 1.5em;
            }
        """)
        layout.addWidget(details_label)

        # Botón de cerrar estilizado
        close_btn = QPushButton("Cerrar")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #6a8caf;
                color: white;
                font-size: 15px;
                border-radius: 10px;
                padding: 8px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #466080;
            }
        """)
        close_btn.clicked.connect(modal.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        opacity_effect = QGraphicsOpacityEffect()
        modal.setGraphicsEffect(opacity_effect)
        self.animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()

        modal.exec()

    def on_table_click(self, index):
        if index.column() != 2:
            return

        fila = index.row()
        nombre = self.model.item(fila, 0).text()

        detalles = {
            "PH": (
                "El pH indica el nivel de acidez o alcalinidad del agua. "
                "Un pH adecuado (5.5 a 6.5 para la mayoría de cultivos hidropónicos) "
                "es fundamental para la absorción óptima de nutrientes. "
                "Valores fuera de rango pueden causar deficiencias o toxicidades en las plantas. "
                "Se recomienda medirlo diariamente y ajustar con soluciones reguladoras si es necesario."
            ),
            "Nutrientes": (
                "Los nutrientes esenciales incluyen nitrógeno (N), fósforo (P), potasio (K), calcio (Ca), magnesio (Mg) y micronutrientes. "
                "La concentración y el equilibrio de estos elementos determinan el crecimiento y la salud de las plantas. "
                "Un exceso o carencia puede provocar síntomas visibles como clorosis, necrosis o bajo rendimiento. "
                "Es importante renovar la solución nutritiva periódicamente y monitorear la conductividad eléctrica (CE)."
            ),
            "Flujo del agua": (
                "El flujo de agua asegura la oxigenación y distribución uniforme de nutrientes. "
                "Un flujo insuficiente puede causar zonas muertas y acumulación de sales, mientras que un flujo excesivo puede dañar raíces. "
                "Se recomienda mantener un flujo constante y revisar periódicamente las bombas y tuberías para evitar obstrucciones."
            ),
            "Nivel del agua": (
                "El nivel de agua debe mantenerse estable para evitar que las raíces se sequen o se ahoguen. "
                "Un nivel bajo puede exponer raíces al aire y causar estrés hídrico, mientras que un nivel alto puede reducir la oxigenación. "
                "Es recomendable usar sensores o inspección visual diaria para ajustar el nivel según las necesidades del sistema y la etapa de cultivo."
            ),
        }

        texto_detalle = detalles.get(nombre, "No hay detalles disponibles para este sensor.")
        self.show_details_modal(nombre, texto_detalle)

    def add_ph_scale(self):
        ph_card = QFrame()
        ph_card.setObjectName("phScaleFrame")
        layout = QVBoxLayout(ph_card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Agregar etiquetas de texto para indicar ácido y alcalino
        labels_layout = QHBoxLayout()
        acid_label = QLabel("Muy Ácido")
        acid_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        neutral_label = QLabel("Neutral")
        neutral_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alkaline_label = QLabel("Muy Alcalino")
        alkaline_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        labels_layout.addWidget(acid_label)
        labels_layout.addStretch()
        labels_layout.addWidget(neutral_label)    
        labels_layout.addStretch()
        labels_layout.addWidget(alkaline_label)
        layout.addLayout(labels_layout)

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

        ph_canvas = FigureCanvas(fig)
        ph_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ph_canvas.setMinimumHeight(150)
        layout.addWidget(ph_canvas)

        self.ph_card = ph_card
