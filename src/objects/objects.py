import sys
from pathlib import Path

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
        
    def addPericia(self, BlocoPericia):
        self.pericias.append(BlocoPericia)    
                    
    def getVida(self):
        return self.BlocoVida.getAtributo()
    
    def setVida(self, vida): 
        print("Set Vida:", vida)
        self.BlocoVida.setAtributo(vida)
        
    def getSanidade(self):
        return self.BlocoSanidade.getAtributo()
    
    def setSanidade(self, sanidade):
        self.BlocoSanidade.setAtributo(sanidade)
        
    def refreshEsforco(self):
        self.BlocoEsforco.setAtributo(self.BlocoEsforco.am1)
        
    def useEsforco(self):
        current = self.BlocoEsforco.getAtributo()
        if current > 0:
            self.BlocoEsforco.setAtributo(current - 1)
            return True
        else:
            return False
    
    
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