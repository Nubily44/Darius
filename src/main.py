import sys

from PySide6.QtWidgets import QApplication

from objects.objects import Personagem, BlocoPericia, Pericia
from interface import Window
from pipes import Pipe

from connectors import handle_esforco_deduct, handle_esforco_refresh, handle_vida, handle_sanidade

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=100, sanidade=100, nivel=10, classe="Classe")
    Personagem1.addPericia(BlocoPericia("Teste", Pericia("Força", 50), Pericia("Destreza", 60), Pericia("Inteligência", 70)))
    window = Window(Personagem1.getVida(), Personagem1.getSanidade(), Personagem1.BlocoEsforco.getAtributo(), Personagem1.getPericias())
    window.set_vida.connect(lambda: handle_vida(Personagem1, window))
    window.set_sanidade.connect(lambda: handle_sanidade(Personagem1, window))
    window.set_esforco.connect(lambda: handle_esforco_deduct(Personagem1, window))
    window.refresh_esforco.connect(lambda: handle_esforco_refresh(Personagem1, window))
    
    window.show()
    sys.exit(app.exec())