import sys
import os  # Importar el módulo 'os'
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QIODevice, QTextStream # Necesario para cargar el QSS
from Calendar import CalendarWindow  # Asumiendo que CalendarWindow está en Calendar/Calendar.py

def main():
    app = QApplication(sys.argv)

    # --- Cargar Hoja de Estilos ---
    try:
        # Obtener el directorio del script actual (Main.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construir la ruta al archivo QSS desde la raíz del proyecto
        qss_relative_path = os.path.join("access", "qss", "styles.qss")
        qss_path = os.path.abspath(os.path.join(script_dir, qss_relative_path))

        print(f"Intentando cargar la hoja de estilos desde (Main.py): {qss_path}") # Para depuración

        qss_file = QFile(qss_path)
        if not qss_file.exists():
            print(f"ERROR (Main.py): El archivo de hoja de estilos NO EXISTE en la ruta: {qss_path}")
        elif qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            app.setStyleSheet(stream.readAll())
            qss_file.close()
            print(f"Hoja de estilos '{qss_path}' cargada correctamente (desde Main.py).")
        else:
            print(f"ERROR (Main.py): No se pudo abrir la hoja de estilos '{qss_path}'.")
            print(f"Razón: {qss_file.errorString()}")

    except Exception as e:
        print(f"Excepción durante la carga de la hoja de estilos (Main.py): {e}")
    # --- Fin Carga de Estilos ---

    window = CalendarWindow()
    window.showMaximized() # Mantienes tu configuración para mostrar maximizado
    sys.exit(app.exec())

if __name__ == "__main__":
    main()