import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import QSize, Signal, Qt
from functions import Wrapper

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
    set_esforco = Signal()
    refresh_esforco = Signal()
    
    def __init__(self, vida, sanidade, esforco):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        self.resize(600, 400)
        
        self.font = QFont("Times", 20)
        self.smallfont = QFont("Times", 14)
        
        self.total = QVBoxLayout(self)
        
        self.bar = QHBoxLayout()
        
        self.container1 = QVBoxLayout()
        self.container2 = QVBoxLayout()
        
        
        self.label_vida = QLabel(f"Vida: {vida}")
        self.label_vida.setFont(self.font)
        
        self.input_vida = QLineEdit()
        self.input_vida.setPlaceholderText("Digite o dano sofrido...")
        self.input_vida.setFixedWidth(300)
        self.input_vida.setFont(self.smallfont)
        
        self.container1.addWidget(self.label_vida, alignment=Qt.AlignCenter | Qt.AlignCenter)
        self.container1.addWidget(self.input_vida, alignment=Qt.AlignCenter | Qt.AlignCenter)
        
        self.label_sanidade = QLabel(f"Sanidade: {sanidade}")
        self.label_sanidade.setFont(self.font)
        self.input_sanidade = QLineEdit()
        self.input_sanidade.setPlaceholderText("Digite o dano sofrido...")
        self.input_sanidade.setFixedWidth(300)
        self.input_sanidade.setFont(self.smallfont)
        
        self.container2.addWidget(self.label_sanidade, alignment=Qt.AlignCenter | Qt.AlignCenter)
        self.container2.addWidget(self.input_sanidade, alignment=Qt.AlignCenter | Qt.AlignCenter)
        
        self.bar.addLayout(self.container1)
        self.bar.addLayout(self.container2)
        self.total.addLayout(self.bar)
        
        self.input_vida.returnPressed.connect(self.set_vida)
        self.input_sanidade.returnPressed.connect(self.set_sanidade)
        
        self.label_esforco = QLabel(f"Esforço: {esforco}")
        self.label_esforco.setFont(self.font)
        self.total.addWidget(self.label_esforco)
        
        self.esforco_deduct = StyledButton(200, 60, "Esforço Gastar", "#cc5632")
        self.total.addWidget(self.esforco_deduct)
        self.esforco_deduct.clicked.connect(self.set_esforco)
        
        self.esforco_refresh = StyledButton(200, 60, "Esforço Renovar", "#32cc6a")
        self.total.addWidget(self.esforco_refresh)
        self.esforco_refresh.clicked.connect(self.refresh_esforco)
        
    @Wrapper
    def setValue(self, label: QLabel, input_field: QLineEdit):
        text = input_field.text()
        before_value = label.text().split(':')[1].strip()
        label.setText(f"{label.text().split(':')[0]}: {int(before_value) - int(text)}")
        input_field.clear()
        return text
    
    def deductValue(self, label: QLabel):
        current = int(label.text().split(':')[1].strip())
        if current > 0:
            label.setText(f"{label.text().split(':')[0]}: {current - 1}")


        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(0, 0, 0)
    window.show()
    sys.exit(app.exec())
