from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QHeaderView, QLabel,
    QVBoxLayout, QDialog, QGraphicsOpacityEffect,
    QStyledItemDelegate
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor, QPen, QBrush, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF, QSize
from PyQt6.uic import loadUi
import os

# Ruta robusta del icono
icon_path = os.path.join(os.path.dirname(__file__), "icons", "menu.png")


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
