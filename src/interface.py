import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import QSize, Signal, Qt, QObject
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

class AttributeObject(QObject):
    
    att_signal = Signal(int)
    
    def __init__(self, name, value, font, smallfont, parent):
        super().__init__(parent)
        self.container = QVBoxLayout()
        self.container.setSpacing(20)
        
        self.label = QLabel(f"{name}: {value}")
        self.label.setFont(font)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Digite o dano sofrido...")
        self.input.setFixedWidth(200)
        self.input.setFont(smallfont)
        
        self.input.returnPressed.connect(self._emit)
        
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
        self.container.addWidget(self.input, alignment=Qt.AlignCenter)

    def _emit(self):
        value = int(self.input.text())
        self.att_signal.emit(value)
        self.input.clear()
    
    def getLayout(self):
        return self.container
    
class UsableObject(QObject):

    usb_use_signal = Signal(int)
    usb_refresh_signal = Signal(int)
    
    def __init__(self, name, value, font, smallfont, parent, maxCount):
        super().__init__(parent)
        self.container = QHBoxLayout()
        
        self.maxCount = maxCount
        
        self.label = QLabel(f"{name}: {value}")
        self.label.setFont(font)
        
        self.deduct = StyledButton(200, 60, "Esforço Gastar", "#cc5632")
        self.refresh = StyledButton(200, 60, "Esforço Renovar", "#32cc6a")
        
        self.deduct.clicked.connect(self._emit_deduct)
        self.refresh.clicked.connect(self._emit_refresh)
        
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
        self.container.addWidget(self.deduct)
        self.container.addWidget(self.refresh)
        
        
    def getLayout(self):
        return self.container
    
    def _emit_deduct(self):
        value = -1
        self.usb_use_signal.emit(value)
        
    def _emit_refresh(self):
        value = self.maxCount
        self.usb_refresh_signal.emit(value)
        
        
class PericiaObject(QObject):
    
    per_use_signal = Signal(str)
    per_use_adv_signal = Signal(str, int)
    
    def __init__(self, name, value, font, smallfont, parent=None):
        super().__init__(parent)
        self.name = name
        self.container = QVBoxLayout()
        #self.container.setSpacing(30)
        self.subcontainer = QHBoxLayout()
        self.btn = StyledButton(150, 50, f"{name} ({value}%)", "#3465d9")
        
        self.label = QLabel(f"Resultado: 0                ")
        self.label.setFont(font)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Vantagem")
        self.input.setFixedWidth(100)
        
        self.btn.clicked.connect(self._emit_use)
        self.input.returnPressed.connect(self._emit_use_adv)

        self.container.addWidget(self.btn, alignment=Qt.AlignCenter)
        self.subcontainer.addWidget(self.input)
        self.subcontainer.addWidget(self.label)
        self.container.addLayout(self.subcontainer)
    
    def getLayout(self):
        return self.container
    
    def _emit_use(self):
        value = self.name
        self.per_use_signal.emit(value)
        
    def _emit_use_adv(self):
        value = self.name
        adv = int(self.input.text()) if self.input.text() else 1
        self.per_use_adv_signal.emit(value, adv)
    
class BlocoPericiasObject:
    def __init__(self, nome, font, smallfont):
        self.container = QVBoxLayout()
        self.label = QLabel(nome)
        self.label.setFont(font)
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
    
    def addPericia(self, pericia_obj: PericiaObject):
        self.container.addLayout(pericia_obj.getLayout())
    
    def getLayout(self):
        return self.container
    

class Window(QWidget):
    
    #set_vida = Signal()
    #set_sanidade = Signal()
    #set_esforco = Signal()
    #refresh_esforco = Signal()
    use_pericia = Signal()
    use_pericia_with_advantage = Signal()
    
    def __init__(self, vida, sanidade, esforco, pericias=None):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        
        self.font = QFont("Times", 18)
        self.smallfont = QFont("Times", 14)
         
        self.total = QVBoxLayout(self)
        
        
        ######## Vida e Sanidade ########
        self.bar = QHBoxLayout()
        self.bar.setContentsMargins(50, 20, 50, 20)
        
        self.interface_vida = AttributeObject("Vida", vida, self.font, self.smallfont, parent=self)      
        self.interface_sanidade = AttributeObject("Sanidade", sanidade, self.font, self.smallfont, parent=self)
        
        self.bar.addLayout(self.interface_vida.getLayout())
        self.bar.addLayout(self.interface_sanidade.getLayout())
        
        self.total.addLayout(self.bar)
        #################################
        
        ############ Esforço ############
        self.esforco_layout = QHBoxLayout()
        self.esforco_layout.setContentsMargins(120, 20, 120, 20)
        self.interface_esforco = UsableObject("Esforço", esforco, self.font, self.smallfont, parent=self, maxCount=esforco)
        
        self.esforco_layout.addLayout(self.interface_esforco.getLayout())
        
        self.total.addLayout(self.esforco_layout)
        #################################
        
        ########### Perícias ############
        self.pericias_total = QVBoxLayout()
        
        self.c4 = QHBoxLayout()
        self.c5 = QHBoxLayout()
        
        self.c4.setContentsMargins(0, 20, 0, 0)
        self.c5.setContentsMargins(0, 20, 0, 0)
        
        self.pericias_array = []
        
        for bloco in pericias:
            
            bloco_layout = BlocoPericiasObject(bloco.nome, self.font, self.smallfont).getLayout()
            bloco_layout.setContentsMargins(20, 0, 20, 0)
            
            for pericia in [bloco.p1, bloco.p2, bloco.p3]:
                pericia_obj = PericiaObject(pericia.nome, pericia.valor, self.font, self.smallfont)
                bloco_layout.addLayout(pericia_obj.getLayout())
                self.pericias_array.append(pericia_obj)
                
            if len(self.c4.children()) < 3:
                self.c4.addLayout(bloco_layout)
            else:
                self.c5.addLayout(bloco_layout)
                
        self.pericias_total.addLayout(self.c4)
        self.pericias_total.addLayout(self.c5)
        
        self.total.addLayout(self.pericias_total)
        
        self.adjustSize()
    
    @Wrapper
    def setValue(self, label: QLabel, value):
        print("Setting value:", value)
        label.setText(f"{label.text().split(':')[0]}: {value}")
        return
    
    
    @Wrapper
    def setValuediff(self, label: QLabel, value):
        print("Setting value:", value)
        before_value = label.text().split(':')[1].strip()
        label.setText(f"{label.text().split(':')[0]}: {int(before_value) - int(value)}")
        return
    
    def searchPericia(self, nome):
        for pericia in self.pericias_array:
            if pericia.name == nome:
                return pericia
        return None


        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(0, 0, 0)
    window.show()
    sys.exit(app.exec())
