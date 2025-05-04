from PyQt6.QtWidgets import (
    QMainWindow, QTableView, QHeaderView, QLabel,
    QVBoxLayout, QDialog, QGraphicsOpacityEffect
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.uic import loadUi


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
