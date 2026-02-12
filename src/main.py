import sys

from PySide6.QtWidgets import QApplication

from objects.personagem import Personagem
from objects.components import BlocoPericia, Pericia
from interface import Window
from functions import Tee
from connectors import handle_esforco_deduct, handle_esforco_refresh, handle_vida, handle_sanidade, handle_pericia_use, handle_pericia_use_adv

def main():
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=100, armor_vida=1, sanidade=100, armor_sanidade=2, nivel=10, classe="Classe")
    
    Personagem1.addPericia(BlocoPericia("Teste", Pericia("Força", 100), Pericia("Destreza", 60), Pericia("Inteligência", 70)))
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
    
    for pericia_obj in window.pericias_array:
        pericia_obj.per_use_signal.connect(lambda value: handle_pericia_use(Personagem1, window, value))
        pericia_obj.per_use_adv_signal.connect(lambda value, adv: handle_pericia_use_adv(Personagem1, window, value, adv))
    
    print("-------------------------------------- SETUP DONE")
    window.show()
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    with open("output.log", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        sys.stdout = Tee(original_stdout, f)
        sys.stderr = Tee(original_stderr, f)

        try:
            main()
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr