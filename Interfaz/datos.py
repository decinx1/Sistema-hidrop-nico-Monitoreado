from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QHeaderView, QLabel,
    QVBoxLayout, QDialog, QGraphicsOpacityEffect,
    QStyledItemDelegate
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.uic import loadUi

class RoundedTextDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        
        # Obtener texto
        text = index.data()
        if not text: 
            painter.restore()
            return

        # Rectángulo del área a dibujar
        rect = QRectF(option.rect.adjusted(8, 8, -8, -8))

        # Estilo redondeado
        bg_color = QColor("#444")  # Color de fondo tipo etiqueta
        text_color = QColor("white")

        # Dibujar fondo redondeado
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 12, 12)

        # Dibujar texto
        painter.setPen(QPen(text_color))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.restore()


class DatosView(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Interfaz/datos.ui", self)

        # Encontrar la tabla
        self.table = self.findChild(QTableView, "tableView")

        # Crear modelo
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Nombre", "Color", "Pin", "Datos", "Detalles."])

        # Datos de ejemplo
        data = [
            ["PH", "", "", "", "⋮"],
            ["Nutrientes", "", "", "", "⋮"],
            ["Flujo del agua", "", "", "", "⋮"],
            ["Nivel del agua", "", "", "", "⋮"],
        ]

        for row_data in data:
            items = [QStandardItem(cell) for cell in row_data]
            for item in items:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.model.appendRow(items)

        self.table.setModel(self.model)
        delegate = RoundedTextDelegate()
        self.table.setItemDelegateForColumn(0, delegate) #se aplica a la columna 0 que es la de nombre


        # Expandir columnas y ajustar altura de filas
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)

        # Conectar clic
        self.table.clicked.connect(self.on_table_click)

    def show_details_modal(self, nombre, texto_detalle):
        # Crear el modal
        modal = QDialog(self)
        modal.setWindowTitle("Detalles")
        modal.setFixedSize(400, 300)
        modal.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Layout del modal
        layout = QVBoxLayout(modal)

        # Label de contenido
        details_label = QLabel(f"<b>{nombre}</b><br><br>{texto_detalle}")
        details_label.setWordWrap(True)

        # Agregar widgets al layout
        layout.addWidget(details_label)

        # Animación de opacidad (fade-in)
        opacity_effect = QGraphicsOpacityEffect()
        modal.setGraphicsEffect(opacity_effect)

        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(400)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()

        modal.exec()

    def on_table_click(self, index):
        if index.column() != 4:  # Columna Detalles
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
