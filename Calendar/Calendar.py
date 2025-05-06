from PyQt6.QtWidgets import (QMainWindow, QWidget, QGridLayout, QPushButton,
                            QLabel, QVBoxLayout, QDialog, QHBoxLayout,
                            QComboBox, QSpinBox, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt, QDate
from conexion_cliente import obtener_datos_por_fecha  # ✅ Importar la función que creamos
from functools import partial


class DayDialog(QDialog):
    last_size = None
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Día {date.toString('dd/MM/yyyy')}")
        # Establecer tamaño dinámico y recordar el último usado
        if DayDialog.last_size:
            self.resize(DayDialog.last_size)
        else:
            self.resize(600, 400)  # Tamaño inicial sugerido

        self.setMinimumSize(400, 300)  # Evita que sea demasiado pequeño

        layout = QVBoxLayout()
        fecha_label = QLabel(date.toString("dddd, dd MMMM yyyy"))
        fecha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(fecha_label)

        # Convertir fecha al formato YYYY-MM-DD para MySQL
        fecha_str = date.toString("yyyy-MM-dd")

        # Obtener datos de la base
        self.resultados = obtener_datos_por_fecha(fecha_str)

        if self.resultados:
            # Obtener lista de sensores únicos
            sensores = sorted(set(sensor for _, sensor, _, _ in self.resultados))
            self.combo_filtro = QComboBox()
            self.combo_filtro.addItem("Todos")
            self.combo_filtro.addItems(sensores)
            self.combo_filtro.currentTextChanged.connect(self.actualizar_tabla)
            layout.addWidget(self.combo_filtro)

            # Crear tabla
            self.tabla = QTableWidget()
            self.tabla.setColumnCount(4)
            self.tabla.setHorizontalHeaderLabels(["ID", "Sensor", "Valor", "Fecha"])
            layout.addWidget(self.tabla)

            # Mostrar todos por defecto
            self.actualizar_tabla("Todos")
        else:
            mensaje = QLabel("No hay datos para esta fecha")
            mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(mensaje)

        self.setLayout(layout)

    def actualizar_tabla(self, sensor_filtrado):
        datos_filtrados = self.resultados if sensor_filtrado == "Todos" else [
            dato for dato in self.resultados if dato[1] == sensor_filtrado
        ]

        self.tabla.setRowCount(len(datos_filtrados))

        for fila, (id_, sensor, valor, fecha) in enumerate(datos_filtrados):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(id_)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(sensor))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(valor)))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(fecha)))

        self.tabla.resizeColumnsToContents()

    def closeEvent(self, event):
        DayDialog.last_size = self.size()  # Guarda el tamaño cuando se cierra
        super().closeEvent(event)


class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendario")
        self.current_date = QDate.currentDate()
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Controles de navegación
        self.create_header(main_layout)
        
        # Días de la semana
        self.create_weekdays_header(main_layout)
        
        # Grid de días
        self.calendar_grid = QGridLayout()
        grid_widget = QWidget()
        grid_widget.setLayout(self.calendar_grid)
        main_layout.addWidget(grid_widget)
        
        self.updateCalendar()
    
    def create_header(self, layout):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        # Botones de navegación
        prev_btn = QPushButton("◀")
        prev_btn.clicked.connect(self.prev_month)
        
        next_btn = QPushButton("▶")
        next_btn.clicked.connect(self.next_month)
        
        # Selectores de mes y año
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
    
    def next_month(self):
        current_month = self.month_combo.currentIndex()
        current_year = self.year_spin.value()
        
        if current_month == 11:
            self.month_combo.setCurrentIndex(0)
            self.year_spin.setValue(current_year + 1)
        else:
            self.month_combo.setCurrentIndex(current_month + 1)
    
    def updateCalendar(self):
        # Limpiar el grid
        for i in reversed(range(self.calendar_grid.count())): 
            self.calendar_grid.itemAt(i).widget().deleteLater()
        
        month = self.month_combo.currentIndex() + 1
        year = self.year_spin.value()
        first_day = QDate(year, month, 1)
        days_in_month = first_day.daysInMonth()
        first_day_weekday = first_day.dayOfWeek() % 7  # 0=Dom, 6=Sáb
        row, col = 0, first_day_weekday
        
        # Días del mes anterior (para completar primera semana)
        prev_month = first_day.addMonths(-1)
        prev_month_days = prev_month.daysInMonth()
        for i in range(first_day_weekday):
            day = prev_month_days - first_day_weekday + i + 1
            btn = self.create_day_button(day, disabled=True)
            self.calendar_grid.addWidget(btn, row, i)
        
        # Días del mes actual
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
        
        # Días del siguiente mes (para completar cuadrícula)
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

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.show()
    sys.exit(app.exec())