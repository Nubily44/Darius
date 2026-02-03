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

class AttributeObject:
    def __init__(self, name, value, font, smallfont):
        self.container = QVBoxLayout()
        
        self.label = QLabel(f"{name}: {value}")
        self.label.setFont(font)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Digite o dano sofrido...")
        self.input.setFixedWidth(300)
        self.input.setFont(smallfont)
        
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
        self.container.addWidget(self.input, alignment=Qt.AlignCenter)
    
    def getLayout(self):
        return self.container
    
class UsableObject:
    def __init__(self, name, value, font, smallfont):
        self.container = QHBoxLayout()
        

        
        self.label = QLabel(f"{name}: {value}")
        self.label.setFont(font)
        
        self.deduct = StyledButton(200, 60, "Esforço Gastar", "#cc5632")
        self.refresh = StyledButton(200, 60, "Esforço Renovar", "#32cc6a")
        
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
        self.container.addWidget(self.deduct)
        self.container.addWidget(self.refresh)
        
        
    def getLayout(self):
        return self.container
        

class Window(QWidget):
    
    set_vida = Signal()
    set_sanidade = Signal()
    set_esforco = Signal()
    refresh_esforco = Signal()
    use_pericia = Signal(str)
    
    def __init__(self, vida, sanidade, esforco, pericias=None):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        self.resize(600, 400)
        
        self.font = QFont("Times", 18)
        self.smallfont = QFont("Times", 14)
         
        self.total = QVBoxLayout(self)
        
        ######## Vida e Sanidade ########
        self.bar = QHBoxLayout()
        
        self.interface_vida = AttributeObject("Vida", vida, self.font, self.smallfont)      
        self.interface_sanidade = AttributeObject("Sanidade", sanidade, self.font, self.smallfont)
        
        self.interface_vida.input.returnPressed.connect(self.set_vida)
        self.interface_sanidade.input.returnPressed.connect(self.set_sanidade)
        
        self.bar.addLayout(self.interface_vida.getLayout())
        self.bar.addLayout(self.interface_sanidade.getLayout())
        
        self.total.addLayout(self.bar)
        #################################
        
        self.interface_esforco = UsableObject("Esforço", esforco, self.font, self.smallfont)
        
        self.interface_esforco.refresh.clicked.connect(self.refresh_esforco)
        self.interface_esforco.deduct.clicked.connect(self.set_esforco)
        
        self.total.addLayout(self.interface_esforco.getLayout())
        
        self.pericias_total = QVBoxLayout()
        self.c4 = QHBoxLayout()
        self.c5 = QHBoxLayout()
        
        self.pericias_interface_objects = {}
        
        for bloco in pericias or []:
            bloco_layout = QVBoxLayout()

            bloco_label = QLabel(bloco.nome)
            bloco_label.setFont(self.font)
            
            bloco_layout.addWidget(bloco_label, alignment=Qt.AlignCenter)
            
            for pericia in [bloco.p1, bloco.p2, bloco.p3]:
                
                pericia_button = StyledButton(150, 50, f"{pericia.nome} ({pericia.valor}%)", "#3465d9")
                pericia_label = QLabel(f"Resultado: 0")
                pericia_label.setFont(self.smallfont)
                pericia_button.clicked.connect(lambda n=pericia.nome: self.use_pericia.emit(n))
                bloco_layout.addWidget(pericia_button, alignment=Qt.AlignCenter)
                bloco_layout.addWidget(pericia_label, alignment=Qt.AlignCenter)
                
            if len(self.c4.children()) < 3:
                self.c4.addLayout(bloco_layout)
            else:
                self.c5.addLayout(bloco_layout)
                
        self.pericias_total.addLayout(self.c4)
        self.pericias_total.addLayout(self.c5)
        
        self.total.addLayout(self.pericias_total)
        
        self.adjustSize()
        
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
