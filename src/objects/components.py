import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))
from functions import Wrapper, update_state
from config import writing
from functions import dice, rolagem_sum, rolagem_expressao

#Sempre criar com quantidade máxima
class BlocoAtributo():
    def __init__(self, nome, att, attm, armor=0):
        self.nome = nome
        self.att = att
        self.attm = attm  # Atributo Máximo
        self.armor = armor
        
    def getAtributo(self):
        return self.att
    
    def getAtributoMax(self):
        return self.attm
    
    def setAtributoLiteral(self, att):
        previous = self.att
        self.att = att
        print(f"    [OBJECT] | Settando {self.nome} de {previous} para {self.att} (literal)")
        
        if writing:
            print (f"     [WRITE] | Updating state: {self.nome} to {self.att}")
            update_state(self.nome, self.att)
                
    def setAtributo(self, att):
        
        previous = self.att
        
        if att < 0:
            print("!")
            self.att = self.att - att
        if att > 0 and att <= self.armor:
            pass
        if att > self.armor:
            print("????")
            self.att = self.att - att + self.armor
        
        print(f"    [OBJECT] | Settando {self.nome} de {previous} para {self.att} (armor: {self.armor})")
        
        if writing:
            print (f"     [WRITE] | Updating state: {self.nome} to {self.att}")
            update_state(self.nome, self.att)
        
    def setliteralAtributo(self, att):
        self.att = att

    def getMaxAtributo(self):
        return self.am1
    
    def getArmor(self):
        return self.armor
        
    
class BlocoPericia():
    def __init__(self, nome, tipo, p1, p2, p3, p4=None):
        self.nome = nome
        self.tipo = tipo
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
                
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

class Item:
    def __init__(self, nome, descricao, tamanho, quantidade=1):
        self.nome = nome
        self.descricao = descricao
        self.tamanho = tamanho
        self.quantidade = quantidade

    def __hash__(self):
        return hash(self.nome)

    def __eq__(self, other):
        return isinstance(other, Item) and self.nome == other.nome
    
class Arma(Item):
    def __init__(self, nome, descricao, dano, tipo):
        super().__init__(nome, descricao, tamanho="G")
        self.dano = dano
        self.tipo = tipo
        self.last_roll = None
        
    def rollDano(self, res_pericia):
        print(f"    [OBJECT] | Rolando dano de {self.nome} com resultado de perícia: {res_pericia}")

        return rolagem_expressao(self.dano.get(res_pericia))




class Inventario:
    def __init__(self, capacidade=10):
        self.capacidade = capacidade
        self.items = set()
        
    def addItem(self, item):
        if len(self.items) < self.capacidade:
            if item.tamanho == "P":
                if item in self.items:
                    inv_item = self.searchItem(item.nome)
                    inv_item.quantidade += item.quantidade
                    return True
            self.items.add(item)            
            print(f"    [OBJECT] | Adicionado item: {item.nome}")
            return True
        else:
            print("    [OBJECT] | Inventário cheio! Não é possível adicionar:", item.nome)
            return False
        
    def searchItem(self, nome_item):
        for item in self.items:
            if item.nome == nome_item:
                return item
        return None
    
    def listItems(self):
        print("    [OBJECT] | Itens no Inventário:", [(item.nome, item.quantidade) for item in self.items])
        return list(self.items)
    
    def returnInventory(self):
        return self.items
    
        
    
if __name__ == "__main__":
    print(rolagem_expressao("0"))
    
    arma = Arma("Espada Longa", "desc", {"Desastre": "0", "Falha": "0", "Normal": "1D8", "Bom": "1D8+2", "Extremo": "1D8+4", "Crítico": "1D8+6"}, "Armas Brancas G")
    print(arma.rollDano("Bom"))
    print(arma.rollDano("Extremo"))
    print(arma.rollDano("Crítico"))
    
    inv = Inventario(2)
    item1 = Item("Poção de Cura", "Restaura 2D6+2 de Vida", "P", quantidade=2)
    inv.addItem(item1)
    inv.addItem(item1)
    inv.addItem(arma)
    inv.addItem(arma)
    
    inv.listItems()