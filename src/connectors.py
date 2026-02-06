from dispatcher import Dispatcher
from objects.objects import Personagem
from interface import Window
from functions import Wrapper

@Wrapper
def handle_vida(personagem, window, value):
    Dispatcher(
        lambda p: p.setVida(value),
        lambda p: window.setValuediff(window.interface_vida.label, value),
        2
    ).execute((personagem))

@Wrapper
def handle_sanidade(personagem, window, value):
    Dispatcher(
        lambda p: p.setSanidade(value),
        lambda p: window.setValuediff(window.interface_sanidade.label, value),
        2
    ).execute((personagem))

@Wrapper 
def handle_esforco_deduct(personagem, window, value):
    Dispatcher(
        lambda p: p.useEsforco(),
        lambda p: window.setValue(window.interface_esforco.label, personagem.BlocoEsforco.getAtributo()),
        2
    ).execute((personagem))

@Wrapper
def handle_esforco_refresh(personagem, window, value):
    Dispatcher(
        lambda p: p.refreshEsforco(),
        lambda p: window.interface_esforco.label.setText(f"Esforço: {value}"),
        1
    ).execute((personagem))
    
    
#def handle_pericia_use(personagem, window, pericia_name):
#    Pipe(
#        lambda p: window.
#        lambda p, n: p.usePericia(n),
#        2
#    ).execute((personagem, pericia_name))