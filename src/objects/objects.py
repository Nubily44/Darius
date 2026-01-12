import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))

from functions import dice

class Personagem():
    def __init__(self, vida, sanidade, nivel):
        self.BlocoVida = BlocoAtributo("Vida", vida)
        self.BlocoSanidade = BlocoAtributo("Sanidade", sanidade)
        self.BlocoEsforco = BlocoAtributo("Esforço", nivel)
        
        self.BlocoCorpo_Fisico = BlocoPericia("Corpo Físico", Pericia("Força", 50), Pericia("Destreza", 50), Pericia("Constituição", 50))
        
    def getVida(self):
        return self.vida
    
    def setVida(self, vida): 
        print(dice(6))
        self.vida = vida

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