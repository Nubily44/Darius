import sys
from pathlib import Path
from functions import Wrapper

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from functions import dice

class Personagem():
    def __init__(self, vida, sanidade, nivel, classe):
        self.BlocoVida = BlocoAtributo("Vida", vida)
        self.BlocoSanidade = BlocoAtributo("Sanidade", sanidade)
        self.BlocoEsforco = BlocoAtributo("Esforço", nivel)
        self.Classe = classe
        
        self.pericias = [] # Array de BlocoPericia
        
    @Wrapper
    def addPericia(self, BlocoPericia):
        self.pericias.append(BlocoPericia)    
    
    @Wrapper             
    def getVida(self):
        return self.BlocoVida.getAtributo()
    
    @Wrapper
    def setVida(self, vida):
        nova = self.getVida() - int(vida)
        print("Set Vida:", nova)
        self.BlocoVida.setAtributo(nova)
    
    @Wrapper 
    def getSanidade(self):
        return self.BlocoSanidade.getAtributo()

    @Wrapper
    def setSanidade(self, sanidade):
        print ("Set Sanidade:", sanidade)
        self.BlocoSanidade.setAtributo(sanidade)
    
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
        
    
    
    
class BlocoPericia():
    def __init__(self, nome, p1, p2, p3):
        self.nome = nome
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

#Sempre criar com quantidade máxima
class BlocoAtributo():
    def __init__(self, nome,a1):
        self.nome = nome
        self.a1 = a1
        self.am1 = a1
        
    def getAtributo(self):
        return self.a1
    
    def setAtributo(self, a1):
        self.a1 = a1

    def getMaxAtributo(self):
        return self.am1
        

                
class Pericia():
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor
        
    def getValue(self):
        return self.valor
    
    def setValue(self, valor):
        self.valor = valor
        
    def roll(self, vantagem):
        result = dice(100, vantagem)
        print(result)
        if result <= self.valor/10:
            return 3
        elif result <= self.valor/2:
            return 2
        elif result <= self.valor:
            return 1
        elif result >= 95:
            return -1
        else:
            return 0
        
        
if __name__ == "__main__":

    bp = BlocoPericia("Teste", Pericia("Força", 50), Pericia("Destreza", 60), Pericia("Inteligência", 70))
    print(bp.p1.roll(2))