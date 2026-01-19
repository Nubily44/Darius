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
    set_sanidade = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        self.resize(400, 200)
        
        self.layout = QVBoxLayout(self)
        
        
        self.label1 = QLabel("Vida: 0")
        self.layout.addWidget(self.label1)
        
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("...")
        self.input1.setFixedWidth(200)
        self.layout.addWidget(self.input1)
        
        self.label2 = QLabel("Sanidade: 0")
        self.layout.addWidget(self.label2)
        
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("...")
        self.input2.setFixedWidth(200)
        self.layout.addWidget(self.input2)
        
        self.input1.returnPressed.connect(self.set_vida)
        self.input2.returnPressed.connect(self.set_sanidade)
        
        #self.btn1 = StyledButton(200, 60, "Increment", "#cc5632", "../../contents/Kojima.png")
        #self.layout.addWidget(self.btn1)
        #self.btn1.clicked.connect(self.set_vida)
        
    def setValue(self, label: QLabel, input_field: QLineEdit, value):
        label.setText(f"{label.text().split(':')[0]}: {value}")
        text = input_field.text()
        input_field.clear()
        return text

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
