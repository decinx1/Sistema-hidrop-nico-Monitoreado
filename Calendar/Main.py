import sys
from PyQt6.QtWidgets import QApplication
from Calendar import CalendarWindow  # Asegúrate de que el nombre coincida con tu archivo

def main():
    app = QApplication(sys.argv)
    window = CalendarWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
