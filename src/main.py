import sys

from PySide6.QtWidgets import QApplication

from objects.objects import Personagem
from interface import Window
from pipes import Pipe

def handle_vida(personagem):
    Pipe(
        lambda p: window.setValue(window.label_vida, window.input_vida, p.getVida()),
        lambda p, v: p.setVida(v),
        2
    ).execute((personagem))

def handle_sanidade(personagem):
    Pipe(
        lambda p: window.setValue(window.label_sanidade, window.input_sanidade, p.getSanidade()),
        lambda p, v: p.setSanidade(v),
        2
    ).execute((personagem))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=100, sanidade=100, nivel=10, classe="Classe")
    window = Window()
    window.set_vida.connect(lambda: handle_vida(Personagem1))
    window.set_sanidade.connect(lambda: handle_sanidade(Personagem1))
    
    window.show()
    sys.exit(app.exec())