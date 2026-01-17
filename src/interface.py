import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit
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
    
    set_vida = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        self.resize(1000, 800)
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Value: 0")
        self.layout.addWidget(self.label)
        
        
        #self.btn1 = StyledButton(200, 60, "Increment", "#cc5632", "../../contents/Kojima.png")
        #self.layout.addWidget(self.btn1)
        
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Enter something...")
        self.input1.setFixedWidth(200)
        self.layout.addWidget(self.input1)
        
        self.input1.returnPressed.connect(self.set_vida)
        
        #self.btn1.clicked.connect(self.set_vida)
        
    def setValue(self, value):
        self.label.setText(f"Value: {value}")
        text = self.input1.text()
        self.input1.clear()
        return text
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
