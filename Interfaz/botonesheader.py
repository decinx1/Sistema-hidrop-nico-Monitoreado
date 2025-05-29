from PyQt6.QtWidgets import (
    QWidget, QButtonGroup, QStackedWidget, QDialog, QVBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from datetime import datetime
from Interfaz.conexion_cliente import obtener_todas_las_fechas_y_datos


class BotonesHeaderUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Form")
        self.setGeometry(0, 0, 400, 300)
        self.setWindowTitle("Form")
        self.setStyleSheet("""/* Header completo: botones + buscador */
QPushButton {
    padding: 8px 16px;
    border: 2px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
}
QPushButton:hover {
    border: 2px solid #7db9e8;
    background-color: #f1f1f1;
}
QPushButton:checked {
    background-color: #4CAF50;
    color: white;
    border: 2px solid #4CAF50;
}
QLineEdit {
    padding: 5px 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
}
""")
        # Layout principal
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # Widget contenedor
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # Botón Gráficas
        self.btnHome = QPushButton("Gráficas", self.widget)
        self.btnHome.setObjectName("btnHome")
        self.btnHome.setCheckable(True)
        self.horizontalLayout.addWidget(self.btnHome)
        # Botón Datos
        self.btnDatos = QPushButton("Datos", self.widget)
        self.btnDatos.setObjectName("btnDatos")
        self.btnDatos.setCheckable(True)
        self.horizontalLayout.addWidget(self.btnDatos)
        # Botón Historial
        self.btnHistorial = QPushButton("Historial", self.widget)
        self.btnHistorial.setObjectName("btnHistorial")
        self.btnHistorial.setCheckable(True)
        self.horizontalLayout.addWidget(self.btnHistorial)
        # Campo de texto para búsqueda
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Buscar...")
        self.lineEdit.setMinimumHeight(35)
        self.lineEdit.setMaximumWidth(500)
        self.horizontalLayout.addWidget(self.lineEdit)
        # Botón de búsqueda
        self.btnBuscar = QPushButton("Buscar", self.widget)
        self.btnBuscar.setObjectName("btnBuscar")
        self.horizontalLayout.addWidget(self.btnBuscar)
        # Añadir layout al widget principal
        self.horizontalLayout_2.addWidget(self.widget)

        # Grupo de botones
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.btnHome)
        self.button_group.addButton(self.btnDatos)
        self.button_group.addButton(self.btnHistorial)
        self.btnHome.setChecked(True)
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self._on_button_clicked)
        # Asignar iconos solo si existen (evita retrasos si no existen)
        import os
        iconos = {
            self.btnHome: "Interfaz/icons/grafica.png",
            self.btnDatos: "Interfaz/icons/info.png",
            self.btnHistorial: "Interfaz/icons/historial.png"
        }
        for btn, icon_path in iconos.items():
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
        # Botón de búsqueda
        self.btnBuscar.setStyleSheet("background-color: #4CAF50; color: white;")  # <-- LÍNEA AGREGADA
        self.btnBuscar.clicked.connect(self.realizar_busqueda)

    def realizar_busqueda(self):
        palabra_clave = self.lineEdit.text().strip()

        if not palabra_clave:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingresa una palabra clave para buscar.")
            return

        resultados = self.buscar_por_palabra_clave(palabra_clave)

        if resultados:
            self.abrir_modal(resultados)
        else:
            QMessageBox.information(self, "Sin resultados",
                                    f"No se encontraron datos con la palabra clave '{palabra_clave}'.")

    def buscar_por_palabra_clave(self, palabra_clave):
        datos_por_fecha = obtener_todas_las_fechas_y_datos()
        coincidencias = {}

        # Convertir palabra clave si parece una fecha en formato dd/mm/yyyy
        palabra_clave_normalizada = palabra_clave
        try:
            fecha_convertida = datetime.strptime(palabra_clave, "%d/%m/%Y").strftime("%Y-%m-%d")
            palabra_clave_normalizada = fecha_convertida
        except ValueError:
            pass  # No es una fecha en formato dd/mm/yyyy

        for fecha_str, datos in datos_por_fecha.items():
            for dato in datos:
                id_dato = str(dato[0])
                sensor = str(dato[1])
                valor = str(dato[2])
                fecha = str(dato[3])

                if (palabra_clave.lower() in id_dato.lower() or
                        palabra_clave.lower() in sensor.lower() or
                        palabra_clave.lower() in valor.lower() or
                        palabra_clave.lower() in fecha.lower() or
                        palabra_clave.lower() in fecha_str.lower() or
                        palabra_clave_normalizada.lower() in fecha.lower() or
                        palabra_clave_normalizada.lower() in fecha_str.lower()):

                    if fecha_str not in coincidencias:
                        coincidencias[fecha_str] = []
                    coincidencias[fecha_str].append(dato)

        return coincidencias

    def abrir_modal(self, coincidencias):
        dialog = KeywordSearchDialog(coincidencias, self)
        dialog.exec()

    def _on_button_clicked(self, button):
        # Puedes personalizar la acción según el botón presionado
        if button == self.btnHome:
            print("Botón Home presionado")
        elif button == self.btnDatos:
            print("Botón Datos presionado")
        elif button == self.btnHistorial:
            print("Botón Historial presionado")
        # Aquí puedes emitir señales o llamar funciones para cambiar la vista


class KeywordSearchDialog(QDialog):
    def __init__(self, coincidencias, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de búsqueda")
        self.coincidencias = coincidencias
        self.fechas = list(coincidencias.keys())
        self.fechas_por_pagina = 3  # Mostrar 3 fechas a la vez
        self.pagina_actual = 1

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Controles de paginación
        paginacion_layout = QHBoxLayout()
        self.btn_anterior = QPushButton("Anterior")
        self.btn_siguiente = QPushButton("Siguiente")
        self.lbl_pagina = QLabel()

        # ===== ESTILOS PARA LOS BOTONES =====
        estilo_botones = """
            QPushButton {
                background-color: #4CAF50;  /* Color de fondo verde */
                color: white;               /* Texto blanco */
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Color más oscuro al pasar mouse */
            }
            QPushButton:disabled {
                background-color: #cccccc;  /* Color gris cuando está deshabilitado */
                color: #666666;
            }
        """
        self.btn_anterior.setStyleSheet(estilo_botones)
        self.btn_siguiente.setStyleSheet(estilo_botones)
        # ===== FIN DE ESTILOS =====

        self.btn_anterior.clicked.connect(self.ir_anterior)
        self.btn_siguiente.clicked.connect(self.ir_siguiente)

        paginacion_layout.addWidget(self.btn_anterior)
        paginacion_layout.addWidget(self.lbl_pagina)
        paginacion_layout.addWidget(self.btn_siguiente)
        paginacion_layout.addStretch()
        layout.addLayout(paginacion_layout)

        # Widget para contener los resultados
        self.resultados_widget = QWidget()
        self.resultados_layout = QVBoxLayout(self.resultados_widget)
        layout.addWidget(self.resultados_widget)

        self.actualizar_resultados()

    def actualizar_resultados(self):
        # Limpiar resultados anteriores
        for i in reversed(range(self.resultados_layout.count())):
            self.resultados_layout.itemAt(i).widget().setParent(None)

        total_fechas = len(self.fechas)
        total_paginas = max(1, (total_fechas + self.fechas_por_pagina - 1) // self.fechas_por_pagina)
        self.pagina_actual = max(1, min(self.pagina_actual, total_paginas))

        inicio = (self.pagina_actual - 1) * self.fechas_por_pagina
        fin = inicio + self.fechas_por_pagina
        fechas_pagina = self.fechas[inicio:fin]

        for fecha in fechas_pagina:
            datos = self.coincidencias[fecha]

            fecha_label = QLabel(f"Fecha: {fecha}")
            self.resultados_layout.addWidget(fecha_label)

            tabla = QTableWidget()
            tabla.setColumnCount(4)
            tabla.setHorizontalHeaderLabels(["ID", "Sensor", "Valor", "Fecha"])

            for fila, (id_, sensor, valor, fecha_hora) in enumerate(datos):
                tabla.insertRow(fila)
                tabla.setItem(fila, 0, QTableWidgetItem(str(id_)))
                tabla.setItem(fila, 1, QTableWidgetItem(sensor))
                tabla.setItem(fila, 2, QTableWidgetItem(str(valor)))
                tabla.setItem(fila, 3, QTableWidgetItem(str(fecha_hora)))

            self.resultados_layout.addWidget(tabla)

        self.lbl_pagina.setText(f"Página {self.pagina_actual} de {total_paginas}")
        self.btn_anterior.setEnabled(self.pagina_actual > 1)
        self.btn_siguiente.setEnabled(self.pagina_actual < total_paginas)

    def ir_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.actualizar_resultados()

    def ir_siguiente(self):
        total_fechas = len(self.fechas)
        total_paginas = max(1, (total_fechas + self.fechas_por_pagina - 1) // self.fechas_por_pagina)
        if self.pagina_actual < total_paginas:
            self.pagina_actual += 1
            self.actualizar_resultados()
