from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer
from ConexionDB.usuarios import verificar_credenciales


class LoginForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Iniciar Sesión")
        self.setMinimumSize(420, 420)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card frame for shadow effect
        card = QFrame(self)
        card.setStyleSheet('''
            QFrame {
                background: #fff;
                border-radius: 18px;
                border: 1.5px solid #e5e7eb;
                box-shadow: 0 8px 32px rgba(22,163,74,0.10);
            }
        ''')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(18)

        # Título
        self.label_title = QLabel("<b>Bienvenido a HydroTech</b>", self)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 22px; color: #16A34A; margin-bottom: 8px;")
        card_layout.addWidget(self.label_title)

        # Usuario
        self.lineEdit_user = QLineEdit(self)
        self.lineEdit_user.setPlaceholderText("Usuario")
        self.lineEdit_user.setFixedHeight(38)
        self.lineEdit_user.setStyleSheet("font-size: 16px; padding: 8px; border-radius: 8px; border: 1.5px solid #d1d5db;")
        card_layout.addWidget(self.lineEdit_user)

        # Contraseña
        self.lineEdit_pass = QLineEdit(self)
        self.lineEdit_pass.setPlaceholderText("Contraseña")
        self.lineEdit_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_pass.setFixedHeight(38)
        self.lineEdit_pass.setStyleSheet("font-size: 16px; padding: 8px; border-radius: 8px; border: 1.5px solid #d1d5db;")
        card_layout.addWidget(self.lineEdit_pass)

        # Estado
        self.label_status = QLabel("", self)
        self.label_status.setVisible(False)
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setStyleSheet("font-size: 15px; margin-bottom: 4px;")
        card_layout.addWidget(self.label_status)

        # Botón de login
        self.pushButton_login = QPushButton("Iniciar Sesión", self)
        self.pushButton_login.setFixedHeight(40)
        self.pushButton_login.setStyleSheet('''
            QPushButton {
                font-size: 17px;
                background-color: #16A34A;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #22c55e;
            }
        ''')
        card_layout.addWidget(self.pushButton_login)

        # Botón para ir a registro
        self.btn_to_register = QPushButton("¿No tienes cuenta? Regístrate", self)
        self.btn_to_register.setStyleSheet('''
            QPushButton {
                font-size: 15px;
                color: #2563EB;
                background: transparent;
                border: none;
                margin-top: 8px;
            }
            QPushButton:hover {
                color: #1d4ed8;
                text-decoration: underline;
            }
        ''')
        card_layout.addWidget(self.btn_to_register)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        self.pushButton_login.clicked.connect(self.login)
        self.btn_to_register.clicked.connect(self.go_to_register)

    def login(self):
        user = self.lineEdit_user.text()
        password = self.lineEdit_pass.text()

        if verificar_credenciales(user, password):
            self.label_status.setText(f"Bienvenido, {user}")
            self.label_status.setStyleSheet("color: #16A34A; font-size: 15px; margin-bottom: 4px;")
            self.label_status.setVisible(True)
            QTimer.singleShot(800, self.main_window.login_exitoso)
        else:
            self.label_status.setText("Usuario o contraseña incorrectos")
            self.label_status.setStyleSheet("color: #dc2626; font-size: 15px; margin-bottom: 4px;")
            self.label_status.setVisible(True)

    def go_to_register(self):
        self.main_window.cambiar_vista("registro")