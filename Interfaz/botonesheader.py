from PyQt6.QtWidgets import (
    QWidget, QButtonGroup, QStackedWidget, QDialog, QVBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QPushButton
)
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon
from datetime import datetime
from Interfaz.conexion_cliente import obtener_todas_las_fechas_y_datos


class BotonesHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Cargar el diseño desde el archivo UI
        loadUi("ui/botonesHead.ui", self)

        # Grupo de botones
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.findChild(QWidget, "btnHome"))
        self.button_group.addButton(self.findChild(QWidget, "btnDatos"))
        self.button_group.addButton(self.findChild(QWidget, "btnHistorial"))

        # Encuentra botones específicos
        self.btn_home = self.findChild(QWidget, "btnHome")
        self.btn_datos = self.findChild(QWidget, "btnDatos")
        self.btn_historial = self.findChild(QWidget, "btnHistorial")

        # Botón de búsqueda
        self.btn_buscar = self.findChild(QPushButton, "btnBuscar")
        self.btn_buscar.clicked.connect(self.realizar_busqueda)

        # Campo de texto
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.lineEdit.setPlaceholderText("Buscar...")

        self.btn_home.setChecked(True)

        # Asignar iconos
        self.btn_home.setIcon(QIcon("Interfaz/icons/grafica.png"))
        self.btn_datos.setIcon(QIcon("Interfaz/icons/info.png"))
        self.btn_historial.setIcon(QIcon("Interfaz/icons/historial.png"))

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


class KeywordSearchDialog(QDialog):
    def __init__(self, coincidencias, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de búsqueda")
        self.adjustSize()
        self.setMinimumWidth(480)

        layout = QVBoxLayout()

        if coincidencias:
            for fecha, datos in coincidencias.items():
                fecha_label = QLabel(f"Fecha: {fecha}")
                layout.addWidget(fecha_label)

                tabla = QTableWidget()
                tabla.setColumnCount(4)
                tabla.setHorizontalHeaderLabels(["ID", "Sensor", "Valor", "Fecha"])
                tabla.setRowCount(len(datos))

                for fila, dato in enumerate(datos):
                    tabla.setItem(fila, 0, QTableWidgetItem(str(dato[0])))  # ID
                    tabla.setItem(fila, 1, QTableWidgetItem(str(dato[1])))  # Sensor
                    tabla.setItem(fila, 2, QTableWidgetItem(str(dato[2])))  # Valor
                    tabla.setItem(fila, 3, QTableWidgetItem(str(dato[3])))  # Fecha

                layout.addWidget(tabla)
        else:
            layout.addWidget(QLabel("No se encontraron coincidencias para la palabra clave."))

        self.setLayout(layout)
