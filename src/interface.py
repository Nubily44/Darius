import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDialog, QLineEdit, QHBoxLayout
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import QSize, Signal

class StyledButton(QPushButton):
    def __init__(self, width, height, text, color, image_path=None):
        super().__init__()
        
        base_color = QColor(color)
        
        hover_color = base_color.lighter(120)
        
        self.setText(text)
        self.setFixedSize(width, height)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color.name()};
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 16px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: {hover_color.name()};
                font-weight: bold;
            }}
        """)
        if image_path:
            icon = QIcon(image_path)
            self.setIcon(icon)
            self.setIconSize(QSize(height - 20, height - 20))
        
class Window(QWidget):
    
    increment_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        self.resize(1000, 800)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Value: 0")
        
        
        self.btn1 = StyledButton(200, 60, "Increment", "#cc5632", "../contents/Kojima.png")
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.label)
        
        self.btn2 = StyledButton(200, 60, "Set Value", "#4a7abc")
        self.layout.addWidget(self.btn2)

        self.btn2.clicked.connect(self.open_dialog)
        self.btn1.clicked.connect(self.increment_clicked)
        
    def setValue(self, value):
        self.label.setText(f"Value: {value}")
    
    def open_dialog(self):
        dialog = ValueDialog(self)

        if dialog.exec():
            text = dialog.value()

            if text.isdigit():
                self.setValue(int(text))

        
        
        

class ValueDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert value")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter a number")

        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addWidget(QLabel("Value:"))
        layout.addWidget(self.input)
        layout.addLayout(buttons_layout)

    def value(self):
        return self.input.text()
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
