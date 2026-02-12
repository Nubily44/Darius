import sys
from pathlib import Path
from objects.components import BlocoAtributo, BlocoPericia, Pericia
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))
from functions import Wrapper

class Personagem():
    def __init__(self, vida, sanidade, nivel, classe):
        self.BlocoVida = BlocoAtributo("Vida", vida)
        self.BlocoSanidade = BlocoAtributo("Sanidade", sanidade)
        self.BlocoEsforco = BlocoAtributo("Esforço", nivel)
        self.Classe = classe
        
        self.pericias = [] # Array de BlocoPericia
        
    @Wrapper
    def addPericia(self, BlocoPericia):
        for bp in self.pericias:
            if bp.nome == BlocoPericia.nome:
                return
        self.pericias.append(BlocoPericia)    
    
    def getPericias(self):
        return self.pericias
    
    @Wrapper             
    def getVida(self):
        return self.BlocoVida
    
    @Wrapper
    def setVida(self, vida):
        nova = self.getVida().getAtributo() - int(vida)
        print("Set Vida:", nova)
        self.BlocoVida.setAtributo(nova)
    
    @Wrapper 
    def getSanidade(self):
        return self.BlocoSanidade

    @Wrapper
    def setSanidade(self, sanidade):
        nova = self.getSanidade().getAtributo() - int(sanidade)
        print ("Set Sanidade:", nova)
        self.BlocoSanidade.setAtributo(nova)
    
    @Wrapper
    def useEsforco(self):
        print(f"Usando Esforço: {self.BlocoEsforco.getAtributo()-1} / {self.BlocoEsforco.am1}")
        current = self.BlocoEsforco.getAtributo()
        if current > 0:
            self.BlocoEsforco.setAtributo(current - 1)
            return True
        else:
            return False
    
    @Wrapper
    def refreshEsforco(self):
        print(f"Renovando Esforço: {self.BlocoEsforco.getAtributo()} / {self.BlocoEsforco.am1}")
        self.BlocoEsforco.setAtributo(self.BlocoEsforco.am1)
    
    @Wrapper 
    def addPericia(self, bloco_pericia):
        for bp in self.pericias:
            if bp.nome == bloco_pericia.nome:
                return
        self.pericias.append(bloco_pericia)
        
    @Wrapper
    def usePericia(self, nome_pericia, vantagem):
        for bloco in self.pericias:
            for pericia in [bloco.p1, bloco.p2, bloco.p3]:
                if pericia.nome == nome_pericia:
                    print("Usando Perícia:", nome_pericia)
                    return pericia.roll(vantagem)
        return None
    
    @Wrapper
    def searchPericia(self, nome_pericia):
        for bloco in self.pericias:
            for pericia in [bloco.p1, bloco.p2, bloco.p3]:
                if pericia.nome == nome_pericia:
                    return pericia
        return None
