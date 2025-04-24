from PyQt6.QtWidgets import QMainWindow, QTableView, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

class DatosView(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Interfaz/datos.ui", self)

        # Encontrar la tabla
        self.table = self.findChild(QTableView, "tableView")

        # Crear modelo
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Id", "Nombre", "Color", "Pin", "Datos", "Detalles."])

        # Datos de ejemplo
        data = [
            ["1", "PH", "", "", "", "⋮"],
            ["2", "Nutrientes", "", "", "", "⋮"],
            ["3", "Flujo del agua", "", "", "", "⋮"],
            ["4", "Nivel del agua", "", "", "", "⋮"],
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

        # Estilo visual
        self.table.setStyleSheet("""
            QTableView {
                background-color: #a1e236;
                border: none;
                font-size: 16px;
                alternate-background-color: #8fd128;
                selection-background-color: #72bd25;
            }
            QHeaderView::section {
                background-color: #444;
                color: white;
                font-weight: bold;
                padding: 8px;
            }
        """)

        self.table.setAlternatingRowColors(True)
