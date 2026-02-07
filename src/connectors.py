from dispatcher import Dispatcher
from objects.objects import Personagem
from interface import Window
from functions import Wrapper

@Wrapper
def handle_vida(personagem, window, value):
    Dispatcher(
        lambda p: p.setVida(value),
        lambda p: window.setValuediff(window.interface_vida.label, value),
        1
    ).execute((personagem))

@Wrapper
def handle_sanidade(personagem, window, value):
    Dispatcher(
        lambda p: p.setSanidade(value),
        lambda p: window.setValuediff(window.interface_sanidade.label, value),
        1
    ).execute((personagem))

@Wrapper 
def handle_esforco_deduct(personagem, window, value):
    Dispatcher(
        lambda p: p.useEsforco(),
        lambda p: window.setValue(window.interface_esforco.label, personagem.BlocoEsforco.getAtributo()),
        1
    ).execute((personagem))

@Wrapper
def handle_esforco_refresh(personagem, window, value):
    Dispatcher(
        lambda p: p.refreshEsforco(),
        lambda p: window.interface_esforco.label.setText(f"Esforço: {value}"),
        1
    ).execute((personagem))
    

@Wrapper
def handle_pericia_use(personagem, window, value):
    Dispatcher(
        lambda p: p.usePericia(value, 1),
        lambda p: window.setValue(window.searchPericia(value).label, personagem.searchPericia(value).getLastRoll()),
        1
    ).execute((personagem))
    
@Wrapper
def handle_pericia_use_adv(personagem, window, value, adv):
    Dispatcher(
        lambda p: p.usePericia(value, adv),
        lambda p: window.setValue(window.searchPericia(value).label, personagem.searchPericia(value).getLastRoll()),
        1
    ).execute((personagem))
    