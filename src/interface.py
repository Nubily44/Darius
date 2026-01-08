import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize

class StyledButton(QPushButton):
    def __init__(
        self,
        text="",
        width=150,
        height=50,
        bg_color="#FFB6C1",
        hover_color="#FFA6C9",
        text_color="#000000",
        font_size=14,
        font_weight=QFont.Medium,
        radius=12,
        icon_path=None,
        icon_size=24,
        parent=None
    ):
        super().__init__(text, parent)

        # Size
        self.setFixedSize(width, height)

        # Font
        font = QFont()
        font.setPointSize(font_size)
        font.setWeight(font_weight)
        self.setFont(font)

        # Icon (optional)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(icon_size, icon_size))

        # Style
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: {radius}px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
            }}
        """)
        
        
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Styled Button Example")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        button = StyledButton(
            text="Click Me",
            width=200,
            height=60,
            bg_color="#4CAF50",
            hover_color="#45A049",
            text_color="#FFFFFF",
            font_size=16,
            font_weight=QFont.Bold,
            radius=15,
            icon_path="icon.png",  # path to your icon
            icon_size=32
        )

        layout.addWidget(button)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
