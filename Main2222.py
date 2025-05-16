import sys
from PyQt6.QtWidgets import QApplication
from Calendar import CalendarWindow  # Importacion del hisotrial 'calendar'

def main():
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
