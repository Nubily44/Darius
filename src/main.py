import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from objects.personagem import Personagem
from objects.components import BlocoPericia, Pericia
from interface import Window
from functions import Tee, extract_ficha_data
from connectors import handle_esforco_deduct, handle_esforco_refresh, handle_vida, handle_sanidade, handle_pericia_use, handle_pericia_use_adv

import os

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "contents"))

from sheet_pt3 import sheet


def main():
    
    dados_ficha = extract_ficha_data(sheet)
    #for k, v in dados_ficha.items():
    #    print(f"{k}: {v}")
        
    
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=dados_ficha["Vida"], armor_vida=dados_ficha["Armadura"], sanidade=dados_ficha["Sanidade"], armor_sanidade=dados_ficha["Armadura_S"], nivel=dados_ficha["Nivel"], classe="Classe")
    
    # Pericias adicionadas via ficha
    
    Personagem1.addPericia(
        BlocoPericia(
            str(dados_ficha["BP1_N"]+str(dados_ficha["BP1_V"])), 
            Pericia(dados_ficha["BP1_P1_N"], dados_ficha["BP1_P1_V"]), 
            Pericia(dados_ficha["BP1_P2_N"], dados_ficha["BP1_P2_V"]), 
            Pericia(dados_ficha["BP1_P3_N"], dados_ficha["BP1_P3_V"])))
    
    Personagem1.addPericia(
        BlocoPericia(
            str(dados_ficha["BP2_N"]), 
            Pericia(dados_ficha["BP2_P1_N"], dados_ficha["BP2_P1_V"]), 
            Pericia(dados_ficha["BP2_P2_N"], dados_ficha["BP2_P2_V"]), 
            Pericia(dados_ficha["BP2_P3_N"], dados_ficha["BP2_P3_V"])))
    
    Personagem1.addPericia(
        BlocoPericia(
            str(dados_ficha["BP3_N"]), 
            Pericia(dados_ficha["BP3_P1_N"], dados_ficha["BP3_P1_V"]), 
            Pericia(dados_ficha["BP3_P2_N"], dados_ficha["BP3_P2_V"]), 
            Pericia(dados_ficha["BP3_P3_N"], dados_ficha["BP3_P3_V"])))
    
    Personagem1.addPericia(
        BlocoPericia(
            str(dados_ficha["BP4_N"]), 
            Pericia(dados_ficha["BP4_P1_N"], dados_ficha["BP4_P1_V"]), 
            Pericia(dados_ficha["BP4_P2_N"], dados_ficha["BP4_P2_V"]), 
            Pericia(dados_ficha["BP4_P3_N"], dados_ficha["BP4_P3_V"])))
    
    Personagem1.addPericia(
        BlocoPericia(
            str(dados_ficha["BP5_N"]), 
            Pericia(dados_ficha["BP5_P1_N"], dados_ficha["BP5_P1_V"]), 
            Pericia(dados_ficha["BP5_P2_N"], dados_ficha["BP5_P2_V"]), 
            Pericia(dados_ficha["BP5_P3_N"], dados_ficha["BP5_P3_V"])))
    
    Personagem1.addPericia(
        BlocoPericia(
            str(dados_ficha["BP6_N"]), 
            Pericia(dados_ficha["BP6_P1_N"], dados_ficha["BP6_P1_V"]), 
            Pericia(dados_ficha["BP6_P2_N"], dados_ficha["BP6_P2_V"]), 
            Pericia(dados_ficha["BP6_P3_N"], dados_ficha["BP6_P3_V"])))
    
    
    
    
    Personagem1.addPericia(BlocoPericia(str(dados_ficha["BP2_N"]), Pericia("Carisma", 40), Pericia("Sabedoria", 55), Pericia("Constituição", 65)))
    Personagem1.addPericia(BlocoPericia(str(dados_ficha["BP3_N"]), Pericia("Percepção", 70), Pericia("Vontade", 80), Pericia("Agilidade", 90)))
    Personagem1.addPericia(BlocoPericia(str(dados_ficha["BP4_N"]), Pericia("Lábia", 30), Pericia("Furtividade", 45), Pericia("Atletismo", 75)))
    Personagem1.addPericia(BlocoPericia(str(dados_ficha["BP5_N"]), Pericia("Medicina", 60), Pericia("Tecnologia", 50), Pericia("Ciência", 40)))
    Personagem1.addPericia(BlocoPericia(str(dados_ficha["BP6_N"]), Pericia("Sobrevivência", 55), Pericia("Intuição", 65), Pericia("Armas", 85)))
    Personagem1.addPericia(BlocoPericia(str(dados_ficha["BP6_N"]), Pericia("Sobrevivênciaaa", 55), Pericia("Intuição", 65), Pericia("Armas", 85)))
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