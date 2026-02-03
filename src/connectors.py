from pipes import Pipe
from objects.objects import Personagem
from interface import Window
from pipes import Pipe
from functions import Wrapper

@Wrapper
def handle_vida(personagem, window):
    Pipe(
        lambda p: window.setValue(window.interface_vida.label, window.interface_vida.input),
        lambda p, v: p.setVida(v),
        2
    ).execute((personagem))

@Wrapper
def handle_sanidade(personagem, window):
    Pipe(
        lambda p: window.setValue(window.interface_sanidade.label, window.interface_sanidade.input),
        lambda p, v: p.setSanidade(v),
        2
    ).execute((personagem))

@Wrapper 
def handle_esforco_deduct(personagem, window):
    Pipe(
        lambda p: window.deductValue(window.interface_esforco.label),
        lambda p: p.useEsforco(),
        2
    ).execute((personagem))

@Wrapper
def handle_esforco_refresh(personagem, window):
    Pipe(
        lambda p: window.interface_esforco.label.setText(f"Esforço: {p.BlocoEsforco.getMaxAtributo()}"),
        lambda p: p.refreshEsforco(),
        1
    ).execute((personagem))
    
    
#def handle_pericia_use(personagem, window, pericia_name):
#    Pipe(
#        lambda p: window.
#        lambda p, n: p.usePericia(n),
#        2
#    ).execute((personagem, pericia_name))