from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QDialog, QLabel, QVBoxLayout,
    QWidget, QGridLayout, QPushButton, QHBoxLayout, QLineEdit,
    QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, QDate
import sys

class DayDialog(QDialog):
    def __init__(self, date, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Día {date.toString('dd/MM/yyyy')}")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fecha_label = QLabel(date.toString("dddd, dd MMMM yyyy"))
        fecha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(fecha_label)

        datos_dia = datos.get(date, [])

        if not datos_dia:
            layout.addWidget(QLabel("No hay datos para este día."))
        else:
            for texto, valor in datos_dia:
                lbl = QLabel(f"{texto}: {valor}")
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(lbl)

        self.setLayout(layout)

class SearchResultDialog(QDialog):
    def __init__(self, criterio, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Resultados: {criterio}")
        self.setFixedSize(350, 300)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel(f"Resultados para: {criterio}"))

        results = self.buscar_datos(criterio, datos)

        if not results:
            results.append("No se encontraron resultados.")

        for result in results:
            lbl = QLabel(result)
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

        self.setLayout(layout)

    def buscar_datos(self, criterio, datos):
        criterio = criterio.lower()
        resultados = []

        for fecha, registros in datos.items():
            fecha_str = fecha.toString("dd/MM/yyyy").lower()

            if criterio in fecha_str:
                resultados.append(f"🗓 {fecha_str}")
                for k, v in registros:
                    resultados.append(f"• {k}: {v}")
            else:
                for k, v in registros:
                    if criterio in k.lower() or criterio in v.lower():
                        resultados.append(f"🗓 {fecha_str} — {k}: {v}")
        return resultados

class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendario")
        self.current_date = QDate.currentDate()

        self.datos_diarios = {
            
        }

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.create_header(main_layout)
        self.create_search_controls(main_layout)
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

    def create_search_controls(self, layout):
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)

        self.lineEditSearch = QLineEdit()
        self.lineEditSearch.setPlaceholderText("Escribe lo que deseas buscar")

        self.pushButtonSearch = QPushButton("Buscar")
        self.pushButtonSearch.clicked.connect(self.buscar)

        search_layout.addWidget(self.lineEditSearch)
        search_layout.addWidget(self.pushButtonSearch)

        layout.addWidget(search_widget)

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
        for i in reversed(range(self.calendar_grid.count())):
            self.calendar_grid.itemAt(i).widget().deleteLater()

        month = self.month_combo.currentIndex() + 1
        year = self.year_spin.value()
        first_day = QDate(year, month, 1)
        days_in_month = first_day.daysInMonth()
        first_day_weekday = first_day.dayOfWeek() % 7
        row, col = 0, first_day_weekday

        today = QDate.currentDate()

        prev_month = first_day.addMonths(-1)
        prev_month_days = prev_month.daysInMonth()
        for i in range(first_day_weekday):
            day = prev_month_days - first_day_weekday + i + 1
            btn = self.create_day_button(day, disabled=True)
            self.calendar_grid.addWidget(btn, row, i)

        for day in range(1, days_in_month + 1):
            current_date = QDate(year, month, day)
            if current_date > today:
                btn = self.create_day_button(day, disabled=True)
            else:
                btn = self.create_day_button(day)
                btn.clicked.connect(lambda _, d=current_date: self.show_day_details(d))
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
        dialog = DayDialog(date, self.datos_diarios, self)
        dialog.exec()

    def buscar(self):
        criterio = self.lineEditSearch.text()
        if not criterio:
            return
        dialog = SearchResultDialog(criterio, self.datos_diarios, self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.show()
    sys.exit(app.exec())