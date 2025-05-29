from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QSizePolicy
from PyQt6.QtCore import Qt

class UsuarioWindow(QWidget):
    def __init__(self, user_id=None, usuario_simulado=None):
        super().__init__()
        self.setWindowTitle("Mi Perfil")
        self.setMinimumSize(900, 600)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.user_id = user_id or 1
        self.usuario_simulado = usuario_simulado or {
            'nombre': 'Juan Pérez',
            'correo': 'juanperez@email.com',
        }
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card frame ocupa el centro y se expande
        card = QFrame(self)
        card.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0fdf4, stop:1 #bbf7d0);
                border-radius: 32px;
                border: 2px solid #16A34A;
                box-shadow: 0 12px 48px rgba(22,163,74,0.13);
            }
        ''')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(120, 80, 120, 80)
        card_layout.setSpacing(36)

        self.label_title = QLabel("<b>Mi Perfil</b>", self)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 38px; color: #16A34A; margin-bottom: 18px; letter-spacing: 1px;")
        card_layout.addWidget(self.label_title)

        # Nombre
        self.lineEditNombre = QLineEdit(self)
        self.lineEditNombre.setPlaceholderText("Nombre completo")
        self.lineEditNombre.setFixedHeight(56)
        self.lineEditNombre.setStyleSheet("font-size: 24px; padding: 16px; border-radius: 16px; border: 2px solid #d1fae5; background: #fff;")
        card_layout.addWidget(self.lineEditNombre)

        # Correo
        self.lineEditCorreo = QLineEdit(self)
        self.lineEditCorreo.setPlaceholderText("Correo electrónico")
        self.lineEditCorreo.setFixedHeight(56)
        self.lineEditCorreo.setStyleSheet("font-size: 24px; padding: 16px; border-radius: 16px; border: 2px solid #d1fae5; background: #fff;")
        card_layout.addWidget(self.lineEditCorreo)

        # Contraseña
        self.lineEditPass = QLineEdit(self)
        self.lineEditPass.setPlaceholderText("Nueva contraseña (opcional)")
        self.lineEditPass.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEditPass.setFixedHeight(56)
        self.lineEditPass.setStyleSheet("font-size: 24px; padding: 16px; border-radius: 16px; border: 2px solid #d1fae5; background: #fff;")
        card_layout.addWidget(self.lineEditPass)

        # Botón guardar
        self.btnGuardar = QPushButton("Guardar cambios", self)
        self.btnGuardar.setFixedHeight(60)
        self.btnGuardar.setStyleSheet('''
            QPushButton {
                font-size: 28px;
                background-color: #16A34A;
                color: white;
                border-radius: 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #22c55e;
            }
        ''')
        card_layout.addWidget(self.btnGuardar)

        # El card ocupa el centro y se expande
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cargar_datos_usuario()
        self.btnGuardar.clicked.connect(self.guardar_cambios)

    def cargar_datos_usuario(self):
        usuario = self.usuario_simulado
        self.lineEditNombre.setText(usuario['nombre'])
        self.lineEditCorreo.setText(usuario['correo'])
        self.lineEditPass.setText("")

    def guardar_cambios(self):
        nombre = self.lineEditNombre.text().strip()
        correo = self.lineEditCorreo.text().strip()
        password = self.lineEditPass.text().strip()
        if not nombre or not correo:
            QMessageBox.warning(self, "Error", "El nombre y el correo no pueden estar vacíos.")
            return
        self.usuario_simulado['nombre'] = nombre
        self.usuario_simulado['correo'] = correo
        # Si password no está vacío, se actualizaría la contraseña
        QMessageBox.information(self, "Éxito", "Datos actualizados correctamente (simulado).")
        self.lineEditPass.setText("")
