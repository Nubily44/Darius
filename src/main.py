import sys

from PySide6.QtWidgets import QApplication

from objects.objects import Personagem, BlocoPericia, Pericia
from interface import Window

from connectors import handle_esforco_deduct, handle_esforco_refresh, handle_vida, handle_sanidade

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=100, sanidade=100, nivel=10, classe="Classe")
    
    Personagem1.addPericia(BlocoPericia("Teste", Pericia("Força", 50), Pericia("Destreza", 60), Pericia("Inteligência", 70)))
    Personagem1.addPericia(BlocoPericia("Outro Teste", Pericia("Carisma", 40), Pericia("Sabedoria", 55), Pericia("Constituição", 65)))
    Personagem1.addPericia(BlocoPericia("Terceiro Teste", Pericia("Percepção", 70), Pericia("Vontade", 80), Pericia("Agilidade", 90)))
    Personagem1.addPericia(BlocoPericia("Quarto Teste", Pericia("Lábia", 30), Pericia("Furtividade", 45), Pericia("Atletismo", 75)))
    Personagem1.addPericia(BlocoPericia("Quinto Teste", Pericia("Medicina", 60), Pericia("Tecnologia", 50), Pericia("Ciência", 40)))
    Personagem1.addPericia(BlocoPericia("Sexto Teste", Pericia("Sobrevivência", 55), Pericia("Intuição", 65), Pericia("Armas", 85)))
    
    window = Window(Personagem1.getVida(), Personagem1.getSanidade(), Personagem1.BlocoEsforco.getAtributo(), Personagem1.getPericias())
    window.interface_vida.att_signal.connect(lambda value: handle_vida(Personagem1, window, value))
    window.interface_sanidade.att_signal.connect(lambda value: handle_sanidade(Personagem1, window, value))
    window.interface_esforco.usb_use_signal.connect(lambda value: handle_esforco_deduct(Personagem1, window, value))
    window.interface_esforco.usb_refresh_signal.connect(lambda value: handle_esforco_refresh(Personagem1, window, value))
    
    print("-------------------------------------- SETUP DONE")
    window.show()
    sys.exit(app.exec())