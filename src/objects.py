from functions import dice

class Personagem():
    def __init__(self, vida, sanidade):
        self.vida = vida
        
    def getVida(self):
        return self.vida
    
    def setVida(self, vida): 
        print(dice(6))
        self.vida = vida
        
    