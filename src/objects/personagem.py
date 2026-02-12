import sys
from pathlib import Path
from objects.components import BlocoAtributo, BlocoPericia, Pericia
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))
from functions import Wrapper

class Personagem():
    def __init__(self, vida, armor_vida, sanidade, armor_sanidade, nivel, classe):
        self.BlocoVida = BlocoAtributo("Vida", vida, armor=armor_vida)
        self.BlocoSanidade = BlocoAtributo("Sanidade", sanidade, armor=armor_sanidade)
        self.BlocoEsforco = BlocoAtributo("Esforço", nivel)
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
        nova = self.getVida().getAtributo() - int(vida)
        print("    [OBJECT] | Set Vida:", nova)
        self.BlocoVida.setAtributo(nova)
    
    def getSanidade(self):
        return self.BlocoSanidade

    def setSanidade(self, sanidade):
        nova = self.getSanidade().getAtributo() - int(sanidade)
        print ("    [OBJECT] | Set Sanidade:", nova)
        self.BlocoSanidade.setAtributo(nova)
    
    def useEsforco(self):
        print(f"    [OBJECT] | Usando Esforço: {self.BlocoEsforco.getAtributo()-1} / {self.BlocoEsforco.attm}")
        current = self.BlocoEsforco.getAtributo()
        if current > 0:
            self.BlocoEsforco.setAtributo(current - 1)
            return True
        else:
            return False
    
    def refreshEsforco(self):
        print(f"    [OBJECT] | Renovando Esforço: {self.BlocoEsforco.getAtributo()} / {self.BlocoEsforco.attm}")
        self.BlocoEsforco.setAtributo(self.BlocoEsforco.attm)
    
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
            for pericia in [bloco.p1, bloco.p2, bloco.p3]:
                if pericia.nome == nome_pericia:
                    return pericia
        return None
