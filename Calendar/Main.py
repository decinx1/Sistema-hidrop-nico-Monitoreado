import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QIODevice, QTextStream
from Calendar import CalendarWindow

def main():
    app = QApplication(sys.argv)

    # --- Cargar Hoja de Estilos ---
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qss_relative_path = os.path.join("access", "qss", "styles.qss")
        qss_path = os.path.abspath(os.path.join(script_dir, qss_relative_path))
        qss_file = QFile(qss_path)

        if not qss_file.exists():
            # print(f"ERROR (Main.py): El archivo de hoja de estilos NO EXISTE en la ruta: {qss_path}")
            # Puedes decidir si quieres hacer algo más aquí, como registrar el error en un archivo de log
            # o simplemente continuar sin estilos.
            pass # No hacer nada si el archivo no existe y no quieres un print
        elif qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            app.setStyleSheet(stream.readAll())
            qss_file.close()
            # print(f"Hoja de estilos '{qss_path}' cargada correctamente (desde Main.py).")
        else:
            # print(f"ERROR (Main.py): No se pudo abrir la hoja de estilos '{qss_path}'.")
            # print(f"Razón: {qss_file.errorString()}")
            # Aquí también podrías registrar el error en un log si es importante.
            pass # No hacer nada si no se pudo abrir y no quieres un print

    except Exception as e:
        # print(f"Excepción durante la carga de la hoja de estilos (Main.py): {e}")
        # Dejar este print puede ser útil para errores completamente inesperados,
        # o puedes reemplazarlo con un sistema de logging más formal.
        # Si quieres eliminarlo completamente:
        pass
    # --- Fin Carga de Estilos ---

    window = CalendarWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()