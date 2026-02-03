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
        
        # (TOTAL (BAR (C1, C2), C3, Pericias(C4, C5)))
        # C1: Vida
        # C2: Sanidade
        # C3: Esforço
        # C4: Pericias    
        self.total = QVBoxLayout(self)
        
        self.bar = QHBoxLayout()
        
        self.c1 = QVBoxLayout()
        self.c2 = QVBoxLayout()
        
        #### CONTAINERR 1 - VIDA ####
        #self.label_vida = QLabel(f"Vida: {vida}")
        #self.label_vida.setFont(self.font)
        #
        #self.input_vida = QLineEdit()
        #self.input_vida.setPlaceholderText("Digite o dano sofrido...")
        #self.input_vida.setFixedWidth(300)
        #self.input_vida.setFont(self.smallfont)
        
        self.interface_vida = AttributeObject("Vida", vida, self.font, self.smallfont)
        ################################
        
        #### CONTAINER 2 - SANIDADE ####
        self.label_sanidade = QLabel(f"Sanidade: {sanidade}")
        self.label_sanidade.setFont(self.font)
        self.input_sanidade = QLineEdit()
        self.input_sanidade.setPlaceholderText("Digite o dano sofrido...")
        self.input_sanidade.setFixedWidth(300)
        self.input_sanidade.setFont(self.smallfont)
        
        self.c2.addWidget(self.label_sanidade, alignment=Qt.AlignCenter)
        self.c2.addWidget(self.input_sanidade, alignment=Qt.AlignCenter)
        ################################
        
        self.bar.addLayout(self.interface_vida.getLayout())
        self.bar.addLayout(self.c2)
        self.total.addLayout(self.bar)
        
        self.c3 = QHBoxLayout()
        
        self.input_vida.returnPressed.connect(self.set_vida)
        self.input_sanidade.returnPressed.connect(self.set_sanidade)
        
        self.label_esforco = QLabel(f"Esforço: {esforco}")
        self.label_esforco.setFont(self.font)
        self.c3.addWidget(self.label_esforco, alignment=Qt.AlignCenter)
        
        self.esforco_deduct = StyledButton(200, 60, "Esforço Gastar", "#cc5632")
        self.c3.addWidget(self.esforco_deduct)
        self.esforco_deduct.clicked.connect(self.set_esforco)
        
        self.esforco_refresh = StyledButton(200, 60, "Esforço Renovar", "#32cc6a")
        self.c3.addWidget(self.esforco_refresh)
        self.esforco_refresh.clicked.connect(self.refresh_esforco)
        
        self.total.addLayout(self.c3)
        
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
