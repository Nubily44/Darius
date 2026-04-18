import sys
from pathlib import Path
from objects.components import BlocoAtributo, BlocoPericia, Pericia, Inventario, Item, Arma
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))
from functions import Wrapper, update_state
from config import writing

class Personagem():
    def __init__(self, vida, vida_max, armor_vida, sanidade, sanidade_max, armor_sanidade, esforco, nivel, classe):
        print ("Criando personagem com Vida:", vida, "Vida Max:", vida_max, "Armadura Vida:", armor_vida, "Sanidade:", sanidade, "Sanidade Max:", sanidade_max, "Armadura Sanidade:", armor_sanidade, "Esforço:", esforco, "Nível:", nivel, "Classe:", classe)
        self.BlocoVida = BlocoAtributo("Vida", vida, vida_max, armor=armor_vida)
        self.BlocoSanidade = BlocoAtributo("Sanidade", sanidade, sanidade_max, armor=armor_sanidade)
        self.BlocoEsforco = BlocoAtributo("Esforço", esforco, nivel)
        self.BlocoInventario = Inventario(10)
        self.Classe = classe
        
        self.pericias = [] # Array de BlocoPericia
        
    def addPericia(self, BlocoPericia):
        for bp in self.pericias:
            if bp.nome == BlocoPericia.nome:
                return
        self.pericias.append(BlocoPericia)    
    
    def getPericias(self):
        return self.pericias
               
    def getVida(self):
        return self.BlocoVida
    
    def setVida(self, vida):
        self.BlocoVida.setAtributo(vida)
    
    def getSanidade(self):
        return self.BlocoSanidade

    def setSanidade(self, sanidade):
        self.BlocoSanidade.setAtributo(sanidade)
    
    def useEsforco(self):
        current = self.BlocoEsforco.getAtributo()
        if current > 0:
            self.BlocoEsforco.setAtributoLiteral(current - 1)
            return True
        else:
            return False
    
    def refreshEsforco(self):
        self.BlocoEsforco.setAtributoLiteral(self.BlocoEsforco.attm)
    
    def addPericia(self, bloco_pericia):
        for bp in self.pericias:
            if bp.nome == bloco_pericia.nome:
                return
        self.pericias.append(bloco_pericia)
        
    def usePericia(self, nome_pericia, vantagem):
        for bloco in self.pericias:
            for pericia in [bloco.p1, bloco.p2, bloco.p3]:
                if pericia.nome == nome_pericia:
                    print("    [OBJECT] | Usando Perícia:", nome_pericia)
                    return pericia.roll(vantagem)
        return None
    
    def searchPericia(self, nome_pericia):
        for bloco in self.pericias:
            for pericia in [bloco.p1, bloco.p2, bloco.p3, bloco.p4]:
                if pericia is not None:
                    if pericia.nome == nome_pericia:
                        return pericia
        return None
    
    def listPericias(self):
        pericias_list = []
        for bloco in self.pericias:
            pericias_list.extend([bloco.p1.nome, bloco.p2.nome, bloco.p3.nome])
        return pericias_list

    def addItem(self, item):
        self.BlocoInventario.addItem(item)
        
    def removeItem(self, nome_item):
        self.BlocoInventario.removeItem(nome_item)
        
    def listItems(self):
        return [item.nome for item in self.BlocoInventario.itens]

    def searchItem(self, nome_item):
        for item in self.BlocoInventario.itens:
            if item.nome == nome_item:
                return item
        return None

    def ataque (self, arma):
        res_per = self.usePericia(arma.tipo, 1)
        dano = arma.rollDano(res_per)
        print("    [OBJECT] | Resultado do Ataque com", arma.nome, ":", dano)
        return dano
    


if __name__ == "__main__":
    per = Personagem(vida=10, vida_max=10, armor_vida=2, sanidade=8, sanidade_max=8, armor_sanidade=1, esforco=3, nivel=1, classe="Guerreiro")
    per.addPericia(BlocoPericia("Combate Corpo a Corpo", Pericia("Combate 1", 50), Pericia("Armas Brancas G", 80), Pericia("Inteligência", 100)))
    print(per.listPericias())
    per.BlocoInventario.addItem(Arma("Espada Longa", "desc", {"Desastre": "0", "Falha": "0", "Normal": "1D8", "Bom": "1D8+2", "Extremo": "1D8+4", "Crítico": "1D8+6"}, "Armas Brancas G"))
    print(per.ataque(per.BlocoInventario.searchItem("Espada Longa")))