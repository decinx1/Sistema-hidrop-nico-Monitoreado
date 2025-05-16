from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QHeaderView, QLabel,
    QVBoxLayout, QDialog, QGraphicsOpacityEffect,
    QStyledItemDelegate, QFrame, QSizePolicy
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor, QPen, QBrush, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF, QSize
from PyQt6.uic import loadUi
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
        loadUi("ui/datos.ui", self)

        self.table = self.findChild(QTableView, "tableView")

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Nombre", "Datos", "Detalles"])

        data = [
            ["PH", ""],
            ["Nutrientes", ""],
            ["Flujo del agua", ""],
            ["Nivel del agua", ""],
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

        # Crear un layout principal para organizar la tabla y la escala
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)

        # Agregar la escala visual de pH debajo de la tabla
        self.add_ph_scale()
        main_layout.addWidget(self.ph_card)

        # Establecer el layout principal en la ventana
        central_widget = QFrame()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_details_modal(self, nombre, texto_detalle):
        modal = QDialog(self)
        modal.setWindowTitle("Detalles")
        modal.setFixedSize(400, 300)
        modal.setWindowModality(Qt.WindowModality.ApplicationModal)

        layout = QVBoxLayout(modal)
        details_label = QLabel(f"<b>{nombre}</b><br><br>{texto_detalle}")
        details_label.setWordWrap(True)
        layout.addWidget(details_label)

        opacity_effect = QGraphicsOpacityEffect()
        modal.setGraphicsEffect(opacity_effect)

        # GUARDAR la animación en self para evitar que se destruya
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
            "PH": "Detalles de PH: ...",
            "Nutrientes": "Detalles de Nutrientes: ...",
            "Flujo del agua": "Detalles flujo de agua: ...",
            "Nivel del agua": "Detalles de nivel de agua: ...",
        }

        texto_detalle = detalles.get(nombre, "No hay detalles disponibles para este sensor.")
        self.show_details_modal(nombre, texto_detalle)

    # Aquí puedes agregar más métodos o funcionalidades según sea necesario

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

        ph_canvas = FigureCanvas(fig)
        ph_canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ph_canvas.setMinimumHeight(150)
        layout.addWidget(ph_canvas)

        self.ph_card = ph_card
