import sys
import random
import time
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QIcon, QFont, QColor, QGuiApplication
from PySide6.QtCore import QSize, Signal, Qt, QObject, QTimer
from functions import Wrapper

def random_position(window):
    screens = QGuiApplication.screens()
    screen = random.choice(screens)
    geo = screen.availableGeometry()

    x = random.randint(geo.left(), geo.right() - window.width())
    y = random.randint(geo.top(), geo.bottom() - window.height())

    window.move(x, y)

    window.move(x, y)

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
                font-size: 14px;
                padding: 10px;
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

class LabelObject(QLabel):
    def __init__(self, text, font):
        super().__init__(text)
        self.setFont(font)

class AttributeObject(QObject):
    
    att_signal = Signal(int)
    
    def __init__(self, name, value, value_max, armor, font, smallfont, parent):
        super().__init__(parent)
        self.container = QVBoxLayout()
        self.container.setSpacing(20)
        
        self.subcontainer = QHBoxLayout()
        
        self.label = QLabel(f"{name}: {value} / {value_max}")
        self.label.setFont(font)
        
        self.armor_label = QLabel(f"Armadura: {armor}")
        self.armor_label.setFont(font)
        
        self.input_dano = QLineEdit()
        self.input_dano.setPlaceholderText("Dano...")
        self.input_dano.setFixedWidth(75)
        self.input_dano.setFont(smallfont)
        
        self.input_cura = QLineEdit()
        self.input_cura.setPlaceholderText("Cura...")
        self.input_cura.setFixedWidth(75)
        self.input_cura.setFont(smallfont)
        
        self.input_dano.returnPressed.connect(self._emit_dano)
        self.input_cura.returnPressed.connect(self._emit_cura)
        
        self.subcontainer.addWidget(self.input_dano, alignment=Qt.AlignRight)
        self.subcontainer.addWidget(self.input_cura, alignment=Qt.AlignLeft)
        
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
        self.container.addWidget(self.armor_label, alignment=Qt.AlignCenter)
        self.container.addLayout(self.subcontainer)

    def _emit_dano(self):
        value = int(self.input_dano.text())
        if value < 0:
            pass
        else: 
            self.att_signal.emit(value)
            self.input_dano.clear()
        
    def _emit_cura(self):
        value = int(self.input_cura.text())
        if value < 0:
            pass
        else:
            self.att_signal.emit(-value)
            self.input_cura.clear()
    
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
        
        self.deduct = StyledButton(120, 40, "Gastar", "#994329")
        self.refresh = StyledButton(120, 40, "Renovar", "#1b9146")
        
        self.deduct.clicked.connect(self._emit_deduct)
        self.refresh.clicked.connect(self._emit_refresh)
        
        self.container.addWidget(self.label)
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
    
    def __init__(self, name, value, font, smallfont, type, parent=None):
        super().__init__(parent)
        self.name = name
        self.container = QVBoxLayout()
        self.subcontainer = QHBoxLayout()
        if type == "N":
            self.btn = StyledButton(140, 40, f"{name} ({value}%)", "#1F514A")
        if type == "C":
            self.btn = StyledButton(220, 40, f"{name} ({value}%)", "#1F514A")
        
        self.label = QLabel(f"Resultado: 0         ")
        self.label.setFont(font)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Vantagem")
        if type == "N":
            self.input.setFixedWidth(50)
        if type == "C":
            self.input.setFixedWidth(75)
        
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
        self.label.setFixedWidth(250)
        self.container.addWidget(self.label, alignment=Qt.AlignCenter)
    
    def addPericia(self, pericia_obj: PericiaObject):
        self.container.addLayout(pericia_obj.getLayout())
    
    def getLayout(self):
        return self.container

class botaoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Botão")
        self.layout = QVBoxLayout()
        
        self.btn = StyledButton(200, 60, "Botão", "#000000")
        self.btn.clicked.connect(self.handle_click)
        
        self.layout.addWidget(self.btn, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)
        
        self.children = []
    
    def handle_click(self):
        window = botaoWindow()
        window.show()
        random_position(window)
        self.children.append(window)
    

class Window(QWidget):
    
    #set_vida = Signal()
    #set_sanidade = Signal()
    #set_esforco = Signal()
    #refresh_esforco = Signal()
    
    def __init__(self, vida, sanidade, esforco, pericias=None, inventario=None):
        super().__init__()
        self.setWindowTitle("Darius 0.1")
        
        self.font = QFont("Times", 14)
        self.smallfont = QFont("Times", 10)
        self.absolute = QHBoxLayout(self)
        self.total1 = QVBoxLayout(self)
        
        
        ######## Vida e Sanidade ########
        self.bar = QHBoxLayout()
        self.bar.setContentsMargins(50, 20, 50, 20)
        
        self.interface_vida = AttributeObject(vida.nome, vida.getAtributo(), vida.getAtributoMax(), vida.getArmor(), self.font, self.smallfont, parent=self)      
        self.interface_sanidade = AttributeObject(sanidade.nome, sanidade.getAtributo(), sanidade.getAtributoMax(), sanidade.getArmor(), self.font, self.smallfont, parent=self)
        
        self.bar.addLayout(self.interface_vida.getLayout())
        self.bar.addLayout(self.interface_sanidade.getLayout())
        
        self.total1.addLayout(self.bar)
        #################################
        
        ############ Esforço ############
        self.esforco_layout = QHBoxLayout()
        self.esforco_layout.setContentsMargins(120, 20, 120, 20)
        self.interface_esforco = UsableObject("Esforço", esforco, self.font, self.smallfont, parent=self, maxCount=esforco)
        
        self.esforco_layout.addLayout(self.interface_esforco.getLayout())
        
        self.total1.addLayout(self.esforco_layout)
        #################################
        
        ########### Perícias ############
        self.pericias_total = QVBoxLayout()
        
        self.c4 = QHBoxLayout()
        self.c5 = QHBoxLayout()
        
        self.c4.setContentsMargins(0, 20, 0, 0)
        self.c5.setContentsMargins(0, 20, 0, 0)
        
        self.pericias_array = []
        
        self.interface_utility = QHBoxLayout()
        self.interface_utility.setAlignment(Qt.AlignTop)
        
        for bloco in pericias:
            
            bloco_layout = BlocoPericiasObject(bloco.nome, self.font, self.smallfont).getLayout()
            bloco_layout.setContentsMargins(20, 0, 20, 0)
            
            for pericia in [bloco.p1, bloco.p2, bloco.p3, bloco.p4]:
                if pericia is not None:
                    if bloco.tipo == "Pericia N":
                        pericia_obj = PericiaObject(pericia.nome, pericia.valor, self.font, self.smallfont, "N")
                    elif bloco.tipo == "Pericia C":
                        pericia_obj = PericiaObject(pericia.nome, pericia.valor, self.font, self.smallfont, "C")
                    bloco_layout.addLayout(pericia_obj.getLayout())
                    self.pericias_array.append(pericia_obj)
                
            if len(self.c4.children()) < 3:
                self.c4.addLayout(bloco_layout)
            elif len(self.c5.children()) < 3:
                self.c5.addLayout(bloco_layout)
            else:
                self.interface_utility.addLayout(bloco_layout)
                
        self.pericias_total.addLayout(self.c4)
        self.pericias_total.addLayout(self.c5)
        
        self.total1.addLayout(self.pericias_total)
        
        for i in inventario:
            item_object = PericiaObject(i.nome, 100, self.font, self.smallfont, "N")
            self.interface_utility.addLayout(item_object.getLayout())
        
        self.botao = StyledButton(200, 60, "Botão", "#000000")
        self.botao.clicked.connect(self.handle_botao)
        self.total1.addWidget(self.botao, alignment=Qt.AlignCenter)
        
        self.botao_save = []
        self.absolute.addLayout(self.total1)
        
        
        
        #for item in inventario:
        #    item_object = PericiaObject(item.nome, 100, self.font, self.smallfont)
        #    self.interface_utility.addLayout(item_object.getLayout())
        #    self.interface_utility.addWidget(item_object.label)
        #self.test = PericiaObject("Teste", 100, self.font, self.smallfont)
        #self.interface_utility.addLayout(self.test.getLayout())
        
        self.absolute.addLayout(self.interface_utility)
        #self.adjustSize()
    
    @Wrapper
    def setValue(self, label: QLabel, value1, value2=None):
        print(" [INTERFACE] | Setting value:", value1, "/", value2)
    
        base = label.text().split(':')[0]
        dots = [".", "..", "...", "....", "....."]
        index = 0
    
        def animate():
            nonlocal index
            label.setText(f"{base}: {dots[index]}")
            index += 1
    
            if index == len(dots):
                timer.stop()
                if value2 is not None:
                    label.setText(f"{base}: {value1} / {value2}")
                else:
                    label.setText(f"{base}: {value1}")
    
        timer = QTimer()
        timer.timeout.connect(animate)
        timer.start(100) 
    
    def searchPericia(self, nome):
        for pericia in self.pericias_array:
            if pericia.name == nome:
                return pericia
        return None

    def handle_botao(self):
        print("...                                         botão")
        window = botaoWindow()
        window.show()
        self.botao_save.append(window)


        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window(0, 0, 0)
    window.show()
    sys.exit(app.exec())
