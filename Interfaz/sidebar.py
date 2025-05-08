import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSizePolicy, QToolButton, QLabel, QFrame
)
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QColor, QFont
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
        expanded_width: int = 240,
        collapsed_width: int = 60,
        animation_duration: int = 300,
        logo_filename: str = "logeishon 2.png",
        parent=None
    ):
        super().__init__(parent)

        # ✅ DEFAULT ICON FOLDER
        self._icon_folder = icon_folder or os.path.join(os.path.dirname(__file__), "icons")

        # ✅ DEFAULT MENU ITEMS (nuevo)
        self._items = menu_items or [
            ("Home", "home.png"),
            ("Configuración", "config.png"),
            ("Usuario", "Usuario.png"),
            ("Correo", "Correoo.png"),
            ("Notificaciones", "notii.png"),
        ]

        self._w_exp, self._w_col = expanded_width, collapsed_width
        self._anim_dur = animation_duration
        self._is_expanded = True

        self.setFixedWidth(self._w_exp)

        # Color de fondo con paleta
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#E8F5E9"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Setup colors
        self.bg_color = "#E8F5E9"
        self.text_color = "#1E4620"
        self.accent_color = "#4CAF50"
        self.hover_color = "#C8E6C9"
        self.selected_color = "#81C784"
        self.button_bg_color = "#A5D6A7"

        # Setup fonts
        self.title_font = QFont()
        self.title_font.setPointSize(12)
        self.title_font.setBold(True)

        self.menu_font = QFont()
        self.menu_font.setPointSize(10)

        # Layout principal vertical
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Header con logo y nombre de la app
        self._setup_header(logo_filename)

        # Menú de botones
        self._btns = {}
        for text, fname in self._items:
            self.add_item(text, fname)

        self._layout.addStretch()

        # Botón de salida
        self._setup_footer()

        # Aplicar estilos a los botones
        self._apply_styles()

    def _setup_header(self, logo_filename):
        header = QWidget()
        header.setObjectName("sidebarHeader")
        header.setMinimumHeight(80)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 16, 16, 16)
        header_layout.setSpacing(10)

        self._logo_path = os.path.join(self._icon_folder, logo_filename)
        self._logo_lbl = QLabel()
        if os.path.exists(self._logo_path):
            self._set_logo_pixmap(expanded=True)
        self._logo_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._logo_lbl.setFixedSize(40, 40)
        header_layout.addWidget(self._logo_lbl)

        self._app_name = QLabel("Hydrotech")
        self._app_name.setFont(self.title_font)
        self._app_name.setStyleSheet(f"color: {self.text_color};")
        self._app_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        header_layout.addWidget(self._app_name, 1)

        self._btn_toggle = QToolButton()
        toggle_icon = os.path.join(self._icon_folder, "menu.png")
        if os.path.exists(toggle_icon):
            self._btn_toggle.setIcon(QIcon(toggle_icon))
        self._btn_toggle.setIconSize(QSize(24, 24))
        self._btn_toggle.setFixedSize(32, 32)
        self._btn_toggle.setStyleSheet(f"""
            QToolButton {{
                border: none;
                background-color: transparent;
                color: {self.text_color};
            }}
            QToolButton:hover {{
                background-color: {self.hover_color};
                border-radius: 4px;
            }}
        """)
        self._btn_toggle.clicked.connect(self.toggle)
        header_layout.addWidget(self._btn_toggle)

        self._layout.addWidget(header)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(f"background-color: {self.selected_color}; max-height: 1px;")
        self._layout.addWidget(separator)

    def _setup_footer(self):
        footer = QWidget()
        footer.setObjectName("sidebarFooter")
        footer.setMinimumHeight(60)
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(8, 8, 8, 16)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(f"background-color: {self.selected_color}; max-height: 1px;")
        footer_layout.addWidget(separator)

        self._btn_exit = QPushButton("Salir" if self._is_expanded else "")
        exit_icon = os.path.join(self._icon_folder, "exit.png")
        if os.path.exists(exit_icon):
            self._btn_exit.setIcon(QIcon(exit_icon))
        self._btn_exit.setIconSize(QSize(20, 20))
        self._btn_exit.setMinimumHeight(48)
        self._btn_exit.setFont(self.menu_font)
        self._btn_exit.clicked.connect(self._handle_exit)
        footer_layout.addWidget(self._btn_exit)

        self._layout.addWidget(footer)

    def add_item(self, text: str, icon_file: str, callback=None):
        btn = QPushButton(text if self._is_expanded else "")
        path = os.path.join(self._icon_folder, icon_file)
        if os.path.exists(path):
            btn.setIcon(QIcon(path))
        btn.setIconSize(QSize(20, 20))
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setMinimumHeight(48)
        btn.setFont(self.menu_font)
        btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        if callback:
            btn.clicked.connect(callback)
        self._layout.addWidget(btn)
        self._btns[text] = btn
        return btn

    def _apply_styles(self):
        button_style = f"""
            QPushButton {{
                background-color: {self.button_bg_color};
                color: {self.text_color};
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
            QPushButton:checked {{
                background-color: {self.selected_color};
                color: {self.text_color};
            }}
        """

        for btn in self._btns.values():
            btn.setStyleSheet(button_style)

        self._btn_exit.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.button_bg_color};
                color: {self.text_color};
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: #FFCDD2;
                color: #B71C1C;
            }}
        """)

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
        anim.setEasingCurve(QEasingCurve.Type.InOutQuint)
        anim.finished.connect(self._on_anim_done)
        anim.start()

        self._is_expanded = not self._is_expanded
        self.toggled.emit(self._is_expanded)
        self._set_logo_pixmap(expanded=self._is_expanded)
        self._app_name.setVisible(self._is_expanded)

    def _set_logo_pixmap(self, expanded: bool):
        size = 40 if expanded else 32
        pix = QPixmap(self._logo_path).scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self._logo_lbl.setPixmap(pix)

    def _on_anim_done(self):
        for text, btn in self._btns.items():
            btn.setText(text if self._is_expanded else "")
        self._btn_exit.setText("Salir" if self._is_expanded else "")

    def _handle_exit(self):
        self.window().close()