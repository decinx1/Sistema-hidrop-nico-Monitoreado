from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout,
    QDialog, QHBoxLayout, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem,
    QTimeEdit, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QTime
from Calendar.conexion_cliente import obtener_datos_por_fecha
from functools import partial


class DayDialog(QDialog):
    last_size = None

    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Día {date.toString('dd/MM/yyyy')}")

        if DayDialog.last_size:
            self.resize(DayDialog.last_size)
        else:
            self.resize(600, 400)

        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        fecha_label = QLabel(date.toString("dddd, dd MMMM yyyy"))
        fecha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(fecha_label)

        fecha_str = date.toString("yyyy-MM-dd")
        self.resultados = obtener_datos_por_fecha(fecha_str)

        if self.resultados:
            sensores = sorted(set(sensor for _, sensor, _, _ in self.resultados))
            self.combo_filtro = QComboBox()
            self.combo_filtro.addItem("Todos")
            self.combo_filtro.addItems(sensores)
            self.combo_filtro.currentTextChanged.connect(self.resetear_paginacion)
            layout.addWidget(self.combo_filtro)

            hora_layout = QHBoxLayout()
            self.hora_inicio = QTimeEdit()
            self.hora_fin = QTimeEdit()
            self.hora_inicio.setDisplayFormat("HH:mm")
            self.hora_fin.setDisplayFormat("HH:mm")

            self.hora_inicio.setMinimumTime(QTime(0, 0))
            self.hora_inicio.setMaximumTime(QTime(23, 59))
            self.hora_fin.setMinimumTime(QTime(0, 0))
            self.hora_fin.setMaximumTime(QTime(23, 59))

            self.hora_inicio.setTime(QTime(0, 0))
            self.hora_fin.setTime(QTime(23, 59))

            self.hora_inicio.timeChanged.connect(self.resetear_paginacion)
            self.hora_fin.timeChanged.connect(self.resetear_paginacion)

            hora_layout.addWidget(QLabel("Desde:"))
            hora_layout.addWidget(self.hora_inicio)
            hora_layout.addWidget(QLabel("Hasta:"))
            hora_layout.addWidget(self.hora_fin)
            layout.addLayout(hora_layout)

            control_layout = QHBoxLayout()
            self.combo_registros = QComboBox()
            self.combo_registros.addItems(["5", "10", "20"])
            self.combo_registros.setCurrentIndex(0)
            self.combo_registros.currentTextChanged.connect(self.resetear_paginacion)

            control_layout.addWidget(QLabel("Mostrar:"))
            control_layout.addWidget(self.combo_registros)
            control_layout.addStretch()
            layout.addLayout(control_layout)

            self.tabla = QTableWidget()
            self.tabla.setColumnCount(4)
            self.tabla.setHorizontalHeaderLabels(["ID", "Sensor", "Valor", "Fecha"])
            self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            layout.addWidget(self.tabla)

            paginacion_layout = QHBoxLayout()
            self.btn_anterior = QPushButton("Anterior")
            self.btn_siguiente = QPushButton("Siguiente")
            self.lbl_pagina = QLabel()

            self.btn_anterior.clicked.connect(self.ir_anterior)
            self.btn_siguiente.clicked.connect(self.ir_siguiente)

            paginacion_layout.addWidget(self.btn_anterior)
            paginacion_layout.addWidget(self.lbl_pagina)
            paginacion_layout.addWidget(self.btn_siguiente)
            paginacion_layout.addStretch()
            layout.addLayout(paginacion_layout)

            self.pagina_actual = 1
            self.actualizar_tabla()
        else:
            mensaje = QLabel("No hay datos para esta fecha")
            mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(mensaje)

        self.setLayout(layout)

    def resetear_paginacion(self):
        self.pagina_actual = 1
        self.actualizar_tabla()

    def obtener_datos_filtrados(self):
        sensor_filtrado = self.combo_filtro.currentText()
        hora_ini = self.hora_inicio.time().toString("HH:mm")
        hora_fin = self.hora_fin.time().toString("HH:mm")

        datos_filtrados = [
            dato for dato in self.resultados
            if (sensor_filtrado == "Todos" or dato[1] == sensor_filtrado)
            and hora_ini <= str(dato[3]).split()[1][:5] <= hora_fin
        ]
        return datos_filtrados

    def actualizar_tabla(self):
        if not hasattr(self, 'tabla'):
            return

        datos_filtrados = self.obtener_datos_filtrados()
        registros_por_pagina = int(self.combo_registros.currentText())

        total_paginas = max(1, (len(datos_filtrados) + registros_por_pagina - 1) // registros_por_pagina)

        self.pagina_actual = max(1, min(self.pagina_actual, total_paginas))

        inicio = (self.pagina_actual - 1) * registros_por_pagina
        fin = inicio + registros_por_pagina
        datos_pagina = datos_filtrados[inicio:fin]

        self.tabla.setRowCount(len(datos_pagina))

        for fila, (id_, sensor, valor, fecha) in enumerate(datos_pagina):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(id_)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(sensor))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(valor)))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(fecha)))

        self.tabla.resizeColumnsToContents()
        self.lbl_pagina.setText(f"Página {self.pagina_actual} de {total_paginas}")
        self.btn_anterior.setEnabled(self.pagina_actual > 1)
        self.btn_siguiente.setEnabled(self.pagina_actual < total_paginas)

    def ir_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.actualizar_tabla()

    def ir_siguiente(self):
        datos_filtrados = self.obtener_datos_filtrados()
        registros_por_pagina = int(self.combo_registros.currentText())
        total_paginas = max(1, (len(datos_filtrados) + registros_por_pagina - 1) // registros_por_pagina)
        if self.pagina_actual < total_paginas:
            self.pagina_actual += 1
            self.actualizar_tabla()

    def closeEvent(self, event):
        DayDialog.last_size = self.size()
        super().closeEvent(event)

class KeywordSearchDialog(QDialog):
    def __init__(self, coincidencias, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de búsqueda")

        layout = QVBoxLayout()

        if coincidencias:
            for fecha, datos in coincidencias.items():
                fecha_label = QLabel(f"Fecha: {fecha}")
                layout.addWidget(fecha_label)

                tabla = QTableWidget()
                tabla.setColumnCount(4)
                tabla.setHorizontalHeaderLabels(["ID", "Sensor", "Valor", "Fecha"])

                for fila, (id_, sensor, valor, fecha) in enumerate(datos):
                    tabla.insertRow(fila)
                    tabla.setItem(fila, 0, QTableWidgetItem(str(id_)))
                    tabla.setItem(fila, 1, QTableWidgetItem(sensor))
                    tabla.setItem(fila, 2, QTableWidgetItem(str(valor)))
                    tabla.setItem(fila, 3, QTableWidgetItem(str(fecha)))

                layout.addWidget(tabla)
        else:
            mensaje = QLabel("No se encontraron coincidencias para la palabra clave.")
            layout.addWidget(mensaje)

        self.setLayout(layout)



class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendario")
        self.current_date = QDate.currentDate()
        self.initUI()

    def buscar_por_palabra_clave(self, palabra_clave):
        from conexion_cliente import obtener_todas_las_fechas_y_datos

        resultados = obtener_todas_las_fechas_y_datos()

        coincidencias = {}
        for fecha_str, datos in resultados.items():
            for dato in datos:
                if palabra_clave.lower() in dato[1].lower():
                    if fecha_str not in coincidencias:
                        coincidencias[fecha_str] = []
                    coincidencias[fecha_str].append(dato)

        if coincidencias:
            # Mostrar los resultados en un modal
            dialog = KeywordSearchDialog(coincidencias, self)
            dialog.exec()
        else:
            QMessageBox.information(self, "Sin resultados",
                                    f"No se encontraron datos con la palabra clave '{palabra_clave}'.")

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.create_header(main_layout)

        # Buscador y botón de búsqueda
        buscador_layout = QHBoxLayout()
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por fecha (dd/mm/yyyy)")
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_por_fecha)
        buscador_layout.addWidget(self.input_busqueda)
        buscador_layout.addWidget(btn_buscar)
        main_layout.addLayout(buscador_layout)

        self.create_weekdays_header(main_layout)

        self.calendar_grid = QGridLayout()
        grid_widget = QWidget()
        grid_widget.setLayout(self.calendar_grid)
        main_layout.addWidget(grid_widget)

        self.updateCalendar()

    def create_header(self, layout):
        header = QWidget()
        header_layout = QHBoxLayout(header)

        prev_btn = QPushButton("◀")
        prev_btn.clicked.connect(self.prev_month)

        next_btn = QPushButton("▶")
        next_btn.clicked.connect(self.next_month)

        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.month_combo.setCurrentIndex(self.current_date.month() - 1)
        self.month_combo.currentIndexChanged.connect(self.updateCalendar)

        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(self.current_date.year())
        self.year_spin.valueChanged.connect(self.updateCalendar)

        header_layout.addWidget(prev_btn)
        header_layout.addWidget(self.month_combo)
        header_layout.addWidget(self.year_spin)
        header_layout.addWidget(next_btn)

        layout.addWidget(header)

    def create_weekdays_header(self, layout):
        week_days = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
        days_header = QWidget()
        days_layout = QGridLayout(days_header)

        for i, day in enumerate(week_days):
            day_label = QLabel(day)
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            days_layout.addWidget(day_label, 0, i)

        layout.addWidget(days_header)

    def prev_month(self):
        current_month = self.month_combo.currentIndex()
        current_year = self.year_spin.value()

        if current_month == 0:
            self.month_combo.setCurrentIndex(11)
            self.year_spin.setValue(current_year - 1)
        else:
            self.month_combo.setCurrentIndex(current_month - 1)

        self.updateCalendar()

    def next_month(self):
        current_month = self.month_combo.currentIndex()
        current_year = self.year_spin.value()

        if current_month == 11:
            self.month_combo.setCurrentIndex(0)
            self.year_spin.setValue(current_year + 1)
        else:
            self.month_combo.setCurrentIndex(current_month + 1)

        self.updateCalendar()

    def updateCalendar(self):
        for i in reversed(range(self.calendar_grid.count())):
            widget = self.calendar_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        month = self.month_combo.currentIndex() + 1
        year = self.year_spin.value()
        first_day = QDate(year, month, 1)
        days_in_month = first_day.daysInMonth()
        first_day_weekday = first_day.dayOfWeek() % 7

        row, col = 0, first_day_weekday
        prev_month = first_day.addMonths(-1)
        prev_month_days = prev_month.daysInMonth()

        for i in range(first_day_weekday):
            day = prev_month_days - first_day_weekday + i + 1
            btn = self.create_day_button(day, disabled=True)
            self.calendar_grid.addWidget(btn, row, i)

        today = QDate.currentDate()
        for day in range(1, days_in_month + 1):
            current_date = QDate(year, month, day)
            is_today = current_date == today
            is_past = current_date < today

            btn = self.create_day_button(day, not (is_past or is_today))
            if is_past or is_today:
                btn.clicked.connect(partial(self.show_day_details, current_date))

            self.calendar_grid.addWidget(btn, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1

        next_day = 1
        while row < 6 or (row == 6 and col < 7):
            btn = self.create_day_button(next_day, disabled=True)
            self.calendar_grid.addWidget(btn, row, col)
            next_day += 1
            col += 1
            if col > 6:
                col = 0
                row += 1

    def create_day_button(self, day, disabled=False):
        btn = QPushButton(str(day))
        btn.setEnabled(not disabled)
        return btn

    def show_day_details(self, date):
        dialog = DayDialog(date, self)
        dialog.exec()

    def buscar_por_fecha(self):
        texto = self.input_busqueda.text().strip()

        # Intentar interpretar como fecha
        fecha = QDate.fromString(texto, "dd/MM/yyyy")
        if fecha.isValid():
            dialog = DayDialog(fecha, self)
            dialog.exec()
        else:
            # Buscar por palabra clave en todas las fechas disponibles
            self.buscar_por_palabra_clave(texto)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.show()
    sys.exit(app.exec())
