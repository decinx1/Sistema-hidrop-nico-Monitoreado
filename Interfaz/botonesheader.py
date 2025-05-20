from PyQt6.QtWidgets import QWidget, QButtonGroup, QStackedWidget
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIcon

class BotonesHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Cargar el diseño desde el archivo UI
        loadUi("ui/botonesHead.ui", self)

        # Grupo de botones
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.findChild(QWidget, "btnHome"))
        self.button_group.addButton(self.findChild(QWidget, "btnDatos"))
        self.button_group.addButton(self.findChild(QWidget, "btnHistorial"))

        # Encuentra botones específicos
        self.btn_home = self.findChild(QWidget, "btnHome")
        self.btn_datos = self.findChild(QWidget, "btnDatos")
        self.btn_historial = self.findChild(QWidget, "btnHistorial")

        self.btn_home.setChecked(True)
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self._on_button_clicked)

        # Asignar iconos a los botones
        self.btn_home.setIcon(QIcon("Interfaz/icons/grafica.png"))
        self.btn_datos.setIcon(QIcon("Interfaz/icons/info.png"))
        self.btn_historial.setIcon(QIcon("Interfaz/icons/historial.png"))

        # Aplica estilos para el botón seleccionado
        # self._update_button_styles()  # Ya no se usa, todo va por QSS

    def _on_button_clicked(self, button):
        # Asegura que solo un botón esté seleccionado
        for btn in [self.btn_home, self.btn_datos, self.btn_historial]:
            btn.setChecked(btn is button)
        # self._update_button_styles()  # Ya no se usa, todo va por QSS

    # def _update_button_styles(self):
    #     ...eliminado, ahora los estilos van en QSS...
