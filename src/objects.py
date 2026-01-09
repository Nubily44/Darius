class Personagem():
    def __init__(self, vida, sanidade):
        self.vida = vida
        self.sanidade = sanidade
        
    def getvida(self):
        return self.vida
    
    def getsanidade(self):
        return self.sanidade
    
    def setvida(self, vida):
        self.vida = vida
        
    def setsanidade(self, sanidade):
        self.sanidade = sanidade
        
    