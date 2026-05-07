import sys
from pathlib import Path

# Happy Birthday to me!

from PySide6.QtWidgets import QApplication

from objects.personagem import Personagem
from objects.components import BlocoPericia, Pericia, Arma, Item, Inventario
from interface import Window
from functions import Tee, extract_ficha_data, update_state, update_variable, read_state
from connectors import handle_esforco_deduct, handle_esforco_refresh, handle_vida, handle_sanidade, handle_pericia_use, handle_pericia_use_adv, handle_arma_use

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
        update_variable("first_time", False, "src/config.py")
            
    else:
        dados_ficha = read_state()
    
    app = QApplication(sys.argv)
    Personagem1 = Personagem(
        vida=dados_ficha["Vida"],
        vida_max=dados_ficha["Vida_Max"],
        armor_vida=dados_ficha["Armadura"], 
        sanidade=dados_ficha["Sanidade"],
        sanidade_max=dados_ficha["Sanidade_Max"], 
        armor_sanidade=dados_ficha["Armadura_S"], 
        esforco =dados_ficha["Esforço"],
        nivel=dados_ficha["Nivel"], 
        classe="Classe")
    
    # Pericias adicionadas via ficha
    
    for i in range(1, 7):
        Personagem1.addPericia(
            BlocoPericia(
                f"{str(dados_ficha[f"BP{i}_N"])} ({str(dados_ficha[f"BP{i}_V"])})",
                "Pericia N",
                Pericia(dados_ficha[f"BP{i}_P1_N"], dados_ficha[f"BP{i}_P1_V"]),
                Pericia(dados_ficha[f"BP{i}_P2_N"], dados_ficha[f"BP{i}_P2_V"]),
                Pericia(dados_ficha[f"BP{i}_P3_N"], dados_ficha[f"BP{i}_P3_V"]),
            )
        )
    
    Personagem1.addPericia(BlocoPericia("Combate Corpo a Corpo", "Pericia C", Pericia("Combate Direto", 90), Pericia("Assalto", 90), Pericia("Artes Marciais", 90), Pericia("Duelo de Névoa", 90)))
    Personagem1.addPericia(BlocoPericia("Armas de Fogo", "Pericia C", Pericia("Armas de Fogo P", 90), Pericia("Armas de Fogo G", 90), Pericia("Armas de Fogo XL", 90), Pericia("Armas de Fogo Ocultistas", 90)))
    Personagem1.addPericia(BlocoPericia("Armas Brancas", "Pericia C", Pericia("Armas Brancas P", 90), Pericia("Armas Brancas G", 90), Pericia("Armas Brancas XL", 90), Pericia("Armas Brancas Ocultistas", 90)))
    
    Personagem1.BlocoInventario.addItem(Arma("Espada Longa", "desc", {"Desastre": "0", "Falha": "0", "Normal": "1D8", "Bom": "1D8+2", "Extremo": "1D8+4", "Crítico": "1D8+6"}, "Armas Brancas G"))
    Personagem1.BlocoInventario.addItem(Item("Poção de Cura", "Restaura 2D6+2 de Vida", "P", quantidade=2))
    Personagem1.BlocoInventario.addItem(Item("Poção de Sanidade", "Restaura 2D6+2 de Sanidade", "P", quantidade=2))
    Personagem1.BlocoInventario.addItem(Arma("Revólver", "desc", {"Desastre": "0", "Falha": "0", "Normal": "1D10", "Bom": "1D10+2", "Extremo": "1D10+4", "Crítico": "1D10+6"}, "Armas de Fogo P"))
    
    window = Window(Personagem1.getVida(), Personagem1.getSanidade(), Personagem1.BlocoEsforco.getAtributo(), Personagem1.getPericias(), Personagem1.BlocoInventario.returnInventory())
    window.interface_vida.att_signal.connect(lambda value: handle_vida(Personagem1, window, value))
    window.interface_sanidade.att_signal.connect(lambda value: handle_sanidade(Personagem1, window, value))
    
    # Mudar estrutura para reutilizar conexão com utilizáveis do inventário
    window.interface_esforco.usb_use_signal.connect(lambda value: handle_esforco_deduct(Personagem1, window, value))
    window.interface_esforco.usb_refresh_signal.connect(lambda value: handle_esforco_refresh(Personagem1, window, value))
    
    for pericia_obj in window.pericias_array:
        
        pericia_obj.per_use_signal.connect(lambda value: handle_pericia_use(Personagem1, window, value))
        pericia_obj.per_use_adv_signal.connect(lambda value, adv: handle_pericia_use_adv(Personagem1, window, value, adv))
    
    for arma_obj in window.armas_array:
        
        arma_obj.arma_use_signal.connect(lambda value: handle_arma_use(Personagem1, window, value))
    
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