import sys

from PySide6.QtWidgets import QApplication

from objects.objects import Personagem
from interface import Window

def handle_vida(personagem, vida):
    personagem.setVida(vida)
    window.setValue(personagem.getVida())
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=100, sanidade=100)
    window = Window()
    window.increment_clicked.connect(lambda: handle_vida(Personagem1, 25))
    
    window.show()
    sys.exit(app.exec())