from PyQt6.QtWidgets import (QMainWindow, QWidget, QGridLayout, QPushButton, 
                            QLabel, QVBoxLayout, QDialog, QHBoxLayout,
                            QComboBox, QSpinBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

class DayDialog(QDialog):
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalles del día {date.toString('dd/MM/yyyy')}")
        self.setFixedSize(500, 400)  # Ventana más grande
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # <- Esta es la línea que necesitas agregar
        
        # Fecha centrada en la parte superior
        fecha_label = QLabel(f"{date.toString('dddd, dd MMMM yyyy')}")
        fecha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fecha_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(fecha_label)
        
        # Contenedor de los datos del día
        datos_layout = QVBoxLayout()
        datos_layout.setSpacing(15)
        
        ph_label = QLabel("pH: 6.5")
        calidad_label = QLabel("Calidad del agua: Buena")
        temp_label = QLabel("Temperatura: 23°C")
        nivel_label = QLabel("Nivel de agua: 80%")
        
        for lbl in (ph_label, calidad_label, temp_label, nivel_label):
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont("Arial", 14))
            datos_layout.addWidget(lbl)
        
        layout.addLayout(datos_layout)
        layout.addStretch()  # Para dejar espacio al final
        
        self.setLayout(layout)


class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendario")
        self.setFixedSize(700, 500)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QPushButton {
                border: none;
                outline: none;
            }
        """)
        
        self.current_date = QDate.currentDate()
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)  # Eliminamos el espacio entre elementos
        central_widget.setLayout(main_layout)
        
        # Header con controles de fecha
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: #80CC27;
                border-radius: 5px 5px 0 0;
                padding: 10px;
            }
            QLabel, QComboBox, QSpinBox {
                color: white;
                font-size: 14px;
            }
            QComboBox, QSpinBox {
                background-color: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 3px;
                padding: 3px;
                min-width: 60px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 15px;
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(15)
        
        # Controles de mes y año
        self.month_combo = QComboBox()
        self.month_combo.addItems(["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
        self.month_combo.setCurrentIndex(self.current_date.month() - 1)
        self.month_combo.currentIndexChanged.connect(self.updateCalendar)
        
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(self.current_date.year())
        self.year_spin.valueChanged.connect(self.updateCalendar)
        
        # Botones de navegación
        nav_btn_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 0 8px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
                border-radius: 3px;
            }
        """
        
        prev_btn = QPushButton("◀")
        prev_btn.setStyleSheet(nav_btn_style)
        prev_btn.clicked.connect(self.prev_month)
        
        next_btn = QPushButton("▶")
        next_btn.setStyleSheet(nav_btn_style)
        next_btn.clicked.connect(self.next_month)
        
        # Añadir elementos al header
        header_layout.addWidget(prev_btn)
        header_layout.addWidget(self.month_combo)
        header_layout.addWidget(self.year_spin)
        header_layout.addWidget(next_btn)
        header_layout.addStretch()
        
        header.setLayout(header_layout)
        main_layout.addWidget(header)
        
        # Días de la semana (con fondo verde)
        week_days = ["DOM", "LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB"]
        days_header = QWidget()
        days_header.setStyleSheet("""
            QWidget {
                background-color: #80CC27;
            }
            QLabel {
                font-weight: bold;
                color: white;
                padding: 8px 0;
            }
        """)
        
        days_layout = QGridLayout()
        days_layout.setContentsMargins(0, 0, 0, 0)
        days_layout.setHorizontalSpacing(0)
        
        for i, day in enumerate(week_days):
            day_label = QLabel(day)
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            days_layout.addWidget(day_label, 0, i)
        
        days_header.setLayout(days_layout)
        main_layout.addWidget(days_header)
        
        # Grid para los días del mes
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setHorizontalSpacing(0)
        self.calendar_grid.setVerticalSpacing(0)
        
        grid_widget = QWidget()
        grid_widget.setLayout(self.calendar_grid)
        grid_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 0 0 5px 5px;
            }
        """)
        main_layout.addWidget(grid_widget)
        
        self.updateCalendar()
    
    def prev_month(self):
        current_month = self.month_combo.currentIndex()
        current_year = self.year_spin.value()
        
        if current_month == 0:  # Si es enero, retrocedemos a diciembre del año anterior
            self.month_combo.setCurrentIndex(11)
            self.year_spin.setValue(current_year - 1)
        else:
            self.month_combo.setCurrentIndex(current_month - 1)
    
    def next_month(self):
        current_month = self.month_combo.currentIndex()
        current_year = self.year_spin.value()
        
        if current_month == 11:  # Si es diciembre, avanzamos a enero del año siguiente
            self.month_combo.setCurrentIndex(0)
            self.year_spin.setValue(current_year + 1)
        else:
            self.month_combo.setCurrentIndex(current_month + 1)
    
    def updateCalendar(self):
        # Limpiar el grid
        for i in reversed(range(self.calendar_grid.count())): 
            self.calendar_grid.itemAt(i).widget().setParent(None)
        
        # Obtener información del mes actual
        month = self.month_combo.currentIndex() + 1
        year = self.year_spin.value()
        first_day = QDate(year, month, 1)
        days_in_month = first_day.daysInMonth()
        first_day_weekday = first_day.dayOfWeek()  # 1=lun, 7=dom
        
        # Ajustar para que domingo sea la primera columna
        col = first_day_weekday % 7
        row = 0
        
        # Añadir días del mes anterior
        prev_month = first_day.addMonths(-1)
        prev_month_days = prev_month.daysInMonth()
        days_to_show = col  # Cantidad de días del mes anterior a mostrar
        
        for i in range(days_to_show):
            day = prev_month_days - days_to_show + i + 1
            btn = QPushButton(str(day))
            btn.setFixedSize(80, 60)
            btn.setEnabled(False)
            btn.setStyleSheet("""
                QPushButton {
                    color: #CCCCCC;
                    font-size: 14px;
                    background-color: white;
                }
            """)
            self.calendar_grid.addWidget(btn, row, i)
        
        # Añadir días del mes actual
        today = QDate.currentDate()
        
        for day in range(1, days_in_month + 1):
            current_date = QDate(year, month, day)
            is_past = current_date < today
            is_today = current_date == today
            
            btn = QPushButton(str(day))
            btn.setFixedSize(80, 60)
            
            # Estilo base para todos los días
            style = """
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    color: #333333;
                    background-color: white;
                    border: 1px solid #e0e0e0;
                }
            """
            
            if is_past:
                # Días pasados (seleccionables)
                style += """
                    QPushButton:hover {
                        background-color: #E1F5FE;
                        color: #0088CC;
                        border: 1px solid #01ADEF;
                    }
                    QPushButton:pressed {
                        background-color: #B3E5FC;
                        color: #006699;
                    }
                """
                btn.clicked.connect(lambda _, d=current_date: self.showDayDetails(d))
            elif is_today:
                # Día actual
                style = """
                    QPushButton {
                        font-size: 14px;
                        font-weight: bold;
                        color: white;
                        background-color: #FF5722;
                        border: 1px solid #E64A19;
                    }
                """
                btn.clicked.connect(lambda _, d=current_date: self.showDayDetails(d))
            else:
                # Días futuros (no seleccionables)
                btn.setEnabled(False)
                style = """
                    QPushButton {
                        font-size: 14px;
                        color: #CCCCCC;
                        background-color: white;
                        border: 1px solid #e0e0e0;
                    }
                """
            
            btn.setStyleSheet(style)
            self.calendar_grid.addWidget(btn, row, col)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        # Añadir días del siguiente mes para completar la cuadrícula
        next_month_day = 1
        while row < 6 or (row == 6 and col < 7):
            btn = QPushButton(str(next_month_day))
            btn.setFixedSize(80, 60)
            btn.setEnabled(False)
            btn.setStyleSheet("""
                QPushButton {
                    color: #CCCCCC;
                    font-size: 14px;
                    background-color: white;
                    border: 1px solid #e0e0e0;
                }
            """)
            
            self.calendar_grid.addWidget(btn, row, col)
            
            next_month_day += 1
            col += 1
            if col > 6:
                col = 0
                row += 1
    
    def showDayDetails(self, date):
        dialog = DayDialog(date, self)
        dialog.exec()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.show()
    sys.exit(app.exec())