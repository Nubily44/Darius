from functions import dice

class Personagem():
    def __init__(self, vida, sanidade):
        self.vida = vida
        
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