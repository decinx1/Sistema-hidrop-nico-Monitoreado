import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


def apply_styles(app):
    style = """
        QWidget {
            background-color: #FDFDFD;
            color: #121212;
            font-family: 'Segoe UI', sans-serif;
        }

        QPushButton {
            background-color: #00AEEF;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0095D9;
        }

        QPushButton:pressed {
            background-color: #007CB5;
        }

        QLabel {
            color: #121212;
            font-size: 14px;
        }

        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #A1E6F2;
            border-radius: 4px;
            padding: 4px;
            color: #121212;
        }

        QComboBox {
            background-color: #ffffff;
            border: 1px solid #00AEEF;
            border-radius: 4px;
            padding: 4px;
            color: #121212;
        }
    """
    app.setStyleSheet(style)


def apply_icons(window):
    window.HomeButton.setIcon(QIcon("iconos/casita.png"))
    window.HomeButton.setIconSize(QSize(24, 24))

    window.DatosButton.setIcon(QIcon("iconos/grafica.png"))
    window.DatosButton.setIconSize(QSize(24, 24))

    window.HistorialButton.setIcon(QIcon("iconos/historial.png"))
    window.HistorialButton.setIconSize(QSize(24, 24))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_styles(app)

    window = loadUi("home.ui")
    apply_icons(window)

    window.showMaximized()
    sys.exit(app.exec())
