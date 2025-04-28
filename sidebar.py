import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSizePolicy, QToolButton, QLabel
)
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor
from PyQt6.QtCore import (
    QSize, QPropertyAnimation, QEasingCurve,
    pyqtSignal, Qt
)

class Sidebar(QWidget):
    """Sidebar retráctil con logo, botones de menú y botón de salida."""
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        icon_folder: str = None,
        menu_items: list[tuple[str, str]] = None,
        expanded_width: int = 200,
        collapsed_width: int = 50,
        animation_duration: int = 300,
        logo_filename: str = "logo.png",
        parent=None
    ):
        super().__init__(parent)

        # Configuración básica
        self._icon_folder = icon_folder or os.path.join(os.path.dirname(__file__), "icons")
        self._items = menu_items or []
        self._w_exp, self._w_col = expanded_width, collapsed_width
        self._anim_dur = animation_duration
        self._is_expanded = True

        self.setFixedWidth(self._w_exp)

        # Color de fondo con paleta
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#CFFFE5"))  # Fondo verde pastel
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Layout principal vertical
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)

        # Top bar: logo + botón de colapso
        top = QWidget()
        top_l = QHBoxLayout(top)
        top_l.setContentsMargins(8, 8, 8, 8)
        top_l.setSpacing(4)

        logo_path = os.path.join(self._icon_folder, logo_filename)
        logo_lbl = QLabel()
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(
                48, 48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_lbl.setPixmap(pix)
        top_l.addWidget(logo_lbl)

        self._btn_toggle = QToolButton()
        menu_icon = os.path.join(self._icon_folder, "menu.png")
        if os.path.exists(menu_icon):
            self._btn_toggle.setIcon(QIcon(menu_icon))
        self._btn_toggle.setIconSize(QSize(24, 24))
        self._btn_toggle.setCheckable(True)
        self._btn_toggle.setChecked(True)
        self._btn_toggle.clicked.connect(self.toggle)
        top_l.addWidget(self._btn_toggle)

        top_l.addStretch()
        self._layout.addWidget(top)

        # Menú de botones
        self._btns: dict[str, QPushButton] = {}
        for text, fname in self._items:
            self.add_item(text, fname)

        self._layout.addStretch()

        # Botón de salida
        self._btn_exit = QPushButton("Salir" if self._is_expanded else "")
        exit_icon = os.path.join(self._icon_folder, "exit.png")
        if os.path.exists(exit_icon):
            self._btn_exit.setIcon(QIcon(exit_icon))
        self._btn_exit.setIconSize(QSize(16, 16))
        self._btn_exit.setMinimumHeight(40)
        self._btn_exit.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        self._btn_exit.clicked.connect(self._handle_exit)
        self._layout.addWidget(self._btn_exit)

        # Aplicar estilos a los botones
        self.set_button_colors(
            base_color="#CFFFE5",
            hover_color="#A0D6B4",
            checked_color="#82CA9D",
            border_color="#7AC29A"
        )

    def add_item(self, text: str, icon_file: str, callback=None):
        btn = QPushButton(text if self._is_expanded else "")
        path = os.path.join(self._icon_folder, icon_file)
        if os.path.exists(path):
            btn.setIcon(QIcon(path))
        btn.setIconSize(QSize(16, 16))
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setMinimumHeight(40)
        btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        if callback:
            btn.clicked.connect(callback)
        self._layout.addWidget(btn)
        self._btns[text] = btn

    def set_button_colors(self, base_color: str, hover_color: str, checked_color: str, border_color: str = "#CCCCCC"):
        """Estilo bonito para los botones."""
        button_style = f"""
            QPushButton {{
                background-color: {base_color};
                color: #2E2E2E;
                border: 2px solid {border_color};
                border-radius: 10px;
                text-align: left;
                padding-left: 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:checked {{
                background-color: {checked_color};
            }}
        """
        for btn in list(self._btns.values()) + [self._btn_exit]:
            btn.setStyleSheet(button_style)

    def toggle(self):
        start, end = (
            (self._w_exp, self._w_col)
            if self._is_expanded else
            (self._w_col, self._w_exp)
        )
        anim = QPropertyAnimation(self, b"minimumWidth", self)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setDuration(self._anim_dur)
        anim.setEasingCurve(QEasingCurve.Type.OutQuart)  # Animación suave
        anim.finished.connect(self._on_anim_done)
        anim.start()

        self._is_expanded = not self._is_expanded
        self._btn_toggle.setChecked(self._is_expanded)
        self.toggled.emit(self._is_expanded)

    def _on_anim_done(self):
        for text, btn in self._btns.items():
            if self._is_expanded:
                btn.setText(text)
                btn.setStyleSheet(btn.styleSheet() + """
                    text-align: left;
                    padding-left: 12px;
                    color: #2E2E2E;
                    qproperty-iconSize: 16px 16px;
                """)
            else:
                btn.setText(text)
                btn.setStyleSheet(btn.styleSheet() + """
                    text-align: center;
                    padding-left: 0px;
                    color: transparent;
                    qproperty-iconSize: 24px 24px;
                """)
        if self._is_expanded:
            self._btn_exit.setText("Salir")
            self._btn_exit.setStyleSheet(self._btn_exit.styleSheet() + """
                text-align: left;
                padding-left: 12px;
                color: #2E2E2E;
                qproperty-iconSize: 16px 16px;
            """)
        else:
            self._btn_exit.setText("Salir")
            self._btn_exit.setStyleSheet(self._btn_exit.styleSheet() + """
                text-align: center;
                padding-left: 0px;
                color: transparent;
                qproperty-iconSize: 24px 24px;
            """)

    def _handle_exit(self):
        self.window().close()
