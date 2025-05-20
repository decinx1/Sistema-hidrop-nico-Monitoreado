import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import LoginForm
from register import RegisterForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login y Registro")
        self.setFixedSize(400, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Instanciar formularios con referencia a esta ventana
        self.login_form = LoginForm(self)
        self.register_form = RegisterForm(self)

        # Añadir a la pila de widgets
        self.stack.addWidget(self.login_form)     # índice 0
        self.stack.addWidget(self.register_form)  # índice 1

        # Mostrar login por defecto
        self.stack.setCurrentIndex(0)

    def cambiar_vista(self, vista):
        if vista == "login":
            self.stack.setCurrentIndex(0)
        elif vista == "registro":
            self.stack.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())