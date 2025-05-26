from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.uic import loadUi
import os

class UsuarioWindow(QWidget):
    def __init__(self, user_id=None, usuario_simulado=None):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ui', 'usuario.ui')
        loadUi(ui_path, self)
        # Si no hay user_id ni usuario_simulado, usar un usuario simulado por defecto
        self.user_id = user_id or 1
        self.usuario_simulado = usuario_simulado or {
            'nombre': 'Juan Pérez',
            'correo': 'juanperez@email.com',
            # La contraseña no se muestra por seguridad
        }
        self.cargar_datos_usuario()
        self.btnGuardar.clicked.connect(self.guardar_cambios)

    def cargar_datos_usuario(self):
        # Si tuvieras una base de datos, aquí cargarías los datos reales
        usuario = self.usuario_simulado
        self.lineEditNombre.setText(usuario['nombre'])
        self.lineEditCorreo.setText(usuario['correo'])
        self.lineEditPass.setText("")  # Nunca mostrar la contraseña

    def guardar_cambios(self):
        nombre = self.lineEditNombre.text().strip()
        correo = self.lineEditCorreo.text().strip()
        password = self.lineEditPass.text().strip()
        if not nombre or not correo:
            QMessageBox.warning(self, "Error", "El nombre y el correo no pueden estar vacíos.")
            return
        # Aquí iría la lógica para actualizar en la base de datos
        # Por ahora solo simulamos el guardado
        self.usuario_simulado['nombre'] = nombre
        self.usuario_simulado['correo'] = correo
        # Si password no está vacío, se actualizaría la contraseña
        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Éxito", "Datos actualizados correctamente (simulado).")
        self.lineEditPass.setText("")

# ---
# Estructura para uso real:
# class UsuarioWindow(QWidget):
#     def __init__(self, user_id):
#         ...
#         self.user_id = user_id
#         self.cargar_datos_usuario()
#         self.btnGuardar.clicked.connect(self.guardar_cambios)
#
#     def cargar_datos_usuario(self):
#         usuario = obtener_usuario(self.user_id)
#         ...
#     def guardar_cambios(self):
#         ...
#         actualizar_usuario(self.user_id, nombre, correo, password)
#         ...
# ---
