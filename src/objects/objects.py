import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))
from functions import Wrapper
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
        for bp in self.pericias:
            if bp.nome == BlocoPericia.nome:
                return
        self.pericias.append(BlocoPericia)    
    
    def getPericias(self):
        return self.pericias
    
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
        nova = self.getSanidade() - int(sanidade)
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
        print(result)
        if result == 1:
            print("Sucesso Crítico")
            self.last_roll = "Crítico"
            return "Crítico"
        if result <= self.valor/10:
            print("Sucesso Extremo")
            self.last_roll = "Extremo"
            return "Extremo"
        elif result <= self.valor/2:
            print("Sucesso Bom")
            self.last_roll = "Bom"
            return "Bom"
        elif result <= self.valor:
            print("Sucesso Normal")
            self.last_roll = "Normal"
            return "Normal"
        elif result >= 95:
            print("Desastre")
            self.last_roll = "Desastre"
            return "Desastre"
        else:
            print("Falha")
            self.last_roll = "Falha"
            return "Falha"
        
        
if __name__ == "__main__":

    bp = BlocoPericia("Teste", Pericia("Força", 50), Pericia("Destreza", 60), Pericia("Inteligência", 70))
    Personagem1 = Personagem(vida=100, sanidade=100, nivel=10, classe="Classe")
    Personagem1.addPericia(bp)
    Personagem1.addPericia(bp)
    Personagem1.usarPericia("Força", 2)