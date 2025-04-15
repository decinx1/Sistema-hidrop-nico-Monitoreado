from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
from datetime import date as DateToday


class CalendarWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("calendar.ui", self)

        self.configureCalendar()

    def configureCalendar(self):
        today = DateToday.today()

        # Restringe el calendario al día actual
        self.calendarWidget.setMinimumDate(today)
        self.calendarWidget.setMaximumDate(today)
        self.calendarWidget.setSelectedDate(today)
