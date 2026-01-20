from pipes import Pipe
from objects.objects import Personagem
from interface import Window
from pipes import Pipe
from functions import Wrapper

@Wrapper
def handle_vida(personagem, window):
    Pipe(
        lambda p: window.setValue(window.label_vida, window.input_vida),
        lambda p, v: p.setVida(v),
        2
    ).execute((personagem))

@Wrapper
def handle_sanidade(personagem, window):
    Pipe(
        lambda p: window.setValue(window.label_sanidade, window.input_sanidade),
        lambda p, v: p.setSanidade(v),
        2
    ).execute((personagem))

@Wrapper 
def handle_esforco_deduct(personagem, window):
    Pipe(
        lambda p: window.deductValue(window.label_esforco),
        lambda p: p.useEsforco(),
        2
    ).execute((personagem))

@Wrapper
def handle_esforco_refresh(personagem, window):
    Pipe(
        lambda p: window.label_esforco.setText(f"Esforço: {p.BlocoEsforco.getMaxAtributo()}"),
        lambda p: p.refreshEsforco(),
        1
    ).execute((personagem))