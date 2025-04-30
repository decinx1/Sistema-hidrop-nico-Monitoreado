from PyQt6.QtWidgets import QMainWindow, QTableView, QHeaderView, QLabel, QPushButton, QVBoxLayout, QFrame
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

        # Conectar clic
        self.table.clicked.connect(self.on_table_click)

        # Agregar panel de detalles
        self.setup_details_panel()

    def setup_details_panel(self):
        # Crear el panel
        self.details_panel = QFrame(self)
        self.details_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.details_panel.setStyleSheet("background-color: #f0f0f0; border: 2px solid #444; border-radius: 8px;")
        self.details_panel.setVisible(False)

        # Layout del panel
        layout = QVBoxLayout()
        self.details_panel.setLayout(layout)

        # Botón de cerrar
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("font-weight: bold; font-size: 16px; color: red; border: none;")
        self.close_button.clicked.connect(lambda: self.details_panel.setVisible(False))

        # Label de contenido
        self.details_label = QLabel("Aquí se mostrarán los detalles")
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet("font-size: 16px; padding: 10px; color: #444;")

        layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.details_label)

        # Agregar el panel al layout principal
        layout_principal = self.findChild(QVBoxLayout, "verticalLayout")
        layout_principal.addWidget(self.details_panel)

    #al picar 
    def on_table_click(self, index):
        if index.column() == 4:  # Columna Detalles
            fila = index.row()
            nombre = self.model.item(fila, 0).text()
            self.details_label.setText(f"Mostrando detalles del sensor: {nombre}")
            self.details_panel.setVisible(True)
        
        detalles = {
            "PH": "Detalles de PH: ...",
            "Flujo del agua": "Detalles flujo de agua: ...",
            "Nivel del agua": "Detalles de nivel de agua: ...",
        }

        texto_detalle = detalles.get(nombre, "No hay detalles disponibles para este sensor.")
        self.details_label.setText(f"<b>{nombre}</b><br><br>{texto_detalle}")

        self.details_panel.setVisible(True)
