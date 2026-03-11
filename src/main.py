import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from objects.personagem import Personagem
from objects.components import BlocoPericia, Pericia
from interface import Window
from functions import Tee, extract_ficha_data, update_state, update_variable, read_state
from connectors import handle_esforco_deduct, handle_esforco_refresh, handle_vida, handle_sanidade, handle_pericia_use, handle_pericia_use_adv

import os

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "contents"))

from sheet_pt3 import sheet
from config import first_time, writing

def main():
    
    if first_time:
        dados_ficha = extract_ficha_data(sheet)
        for key, value in dados_ficha.items():
            update_state(key, str(value))
        print("Updating variable: 1")
        update_variable("first_time", False, "src/config.py")
            
    else:
        dados_ficha = read_state()
        print("Updating variable: 2")
        update_variable("Vida", 99999, "src/state.log")
        #update_variable("Vida", 1, "src/state.log")
        #update_variable("Vida", 4, "src/state.log")
    
    app = QApplication(sys.argv)
    Personagem1 = Personagem(vida=dados_ficha["Vida"], armor_vida=dados_ficha["Armadura"], sanidade=dados_ficha["Sanidade"], armor_sanidade=dados_ficha["Armadura_S"], nivel=dados_ficha["Nivel"], classe="Classe")
    
    # Pericias adicionadas via ficha
    
    for i in range(1, 7):
        Personagem1.addPericia(
            BlocoPericia(
                f"{str(dados_ficha[f"BP{i}_N"])} ({str(dados_ficha[f"BP{i}_V"])})",
                Pericia(dados_ficha[f"BP{i}_P1_N"], dados_ficha[f"BP{i}_P1_V"], tipo="Perícia"),
                Pericia(dados_ficha[f"BP{i}_P2_N"], dados_ficha[f"BP{i}_P2_V"], tipo="Perícia"),
                Pericia(dados_ficha[f"BP{i}_P3_N"], dados_ficha[f"BP{i}_P3_V"], tipo="Perícia"),
            )
        )
    
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
    with open("src/output.log", "w", encoding="utf-8") as f:
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        sys.stdout = Tee(original_stdout, f)
        sys.stderr = Tee(original_stderr, f)

        try:
            main()
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr