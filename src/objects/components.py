import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))
from functions import Wrapper
from functions import dice

#Sempre criar com quantidade máxima
class BlocoAtributo():
    def __init__(self, nome,att, armor=0):
        self.nome = nome
        self.att = att
        self.attm = att  # Atributo Máximo
        self.armor = armor
        
    def getAtributo(self):
        return self.att
    
    def setAtributo(self, att):
        print(f"    [OBJECT] | Settando {self.nome} de {self.att} para {att + self.armor} (armor: {self.armor})")
        self.att = att + self.armor
        
    def setliteralAtributo(self, att):
        self.att = att

    def getMaxAtributo(self):
        return self.am1
    
    def getArmor(self):
        return self.armor
        
    
class BlocoPericia():
    def __init__(self, nome, p1, p2, p3):
        self.nome = nome
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
                
class Pericia():
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor
        self.last_roll = None
        
    def getValue(self):
        return self.valor
    
    def getLastRoll(self):
        return self.last_roll
    
    def setValue(self, valor):
        self.valor = valor
        
    def roll(self, vantagem):
        result = dice(100, vantagem)
        if result == 1:
            print("    [OBJECT] | Sucesso Crítico")
            self.last_roll = "Crítico"
            return "Crítico"
        if result <= self.valor/10:
            print("    [OBJECT] | Sucesso Extremo")
            self.last_roll = "Extremo"
            return "Extremo"
        elif result <= self.valor/2:
            print("    [OBJECT] | Sucesso Bom")
            self.last_roll = "Bom"
            return "Bom"
        elif result <= self.valor:
            print("    [OBJECT] | Sucesso Normal")
            self.last_roll = "Normal"
            return "Normal"
        elif result >= 95:
            print("    [OBJECT] | Desastre")
            self.last_roll = "Desastre"
            return "Desastre"
        else:
            print("    [OBJECT] | Falha")
            self.last_roll = "Falha"
            return "Falha"