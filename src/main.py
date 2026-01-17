import sys

from PySide6.QtWidgets import QApplication

from objects.objects import Personagem
from interface import Window
from pipes import Pipe

def handle_vida2(personagem, vida):
    Pipe(
        lambda p, v: p.setVida(v),
        lambda p, v: window.setValue(p.getVida()),
        2
    ).execute((personagem, vida))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=100, sanidade=100, nivel=10, classe="Classe")
    window = Window()
    window.increment_clicked.connect(lambda: handle_vida2(Personagem1, 25))
    
    window.show()
    sys.exit(app.exec())