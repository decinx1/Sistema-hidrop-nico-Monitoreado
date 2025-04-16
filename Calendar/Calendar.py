from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
from datetime import date as DateToday, timedelta


class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("calendar.ui", self)  # Llamado del archivo .ui que da Qt Designer

        # Fecha inicial fija
        self.start_date = DateToday(2025, 4, 15)  # Puedes ajustarla
        self.current_day = DateToday.today()

        self.configureCalendar()

        # Si tienes un botón en tu UI llamado btnAvanzar, descomenta esta línea:
        # self.btnAvanzar.clicked.connect(self.avanzarUnDia)

    def configureCalendar(self):
        # Establece el rango desde el 15/04/2025 hasta el día actual
        self.calendarWidget.setMinimumDate(self.start_date)
        self.calendarWidget.setMaximumDate(self.current_day)
        self.calendarWidget.setSelectedDate(self.current_day)

    def avanzarUnDia(self):
        # Incrementa el día actual en uno
        self.current_day += timedelta(days=1)

        # Actualiza el calendario para que permita hasta el nuevo día
        self.calendarWidget.setMaximumDate(self.current_day)
        self.calendarWidget.setSelectedDate(self.current_day)
