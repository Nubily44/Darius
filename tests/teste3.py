sheet = """---------------------------------- Ficha Do Personagem ---------------------------------- ( ( Pt 3 ) )

                                                             Estado  (Nível: 09)

               Vida: (65) // (00)

                Sanidade: (75) // (67)

                   Esforço: 9 

                Armadura: 13

               Armadura de sanidade: 5 (já foi com Deus)
 
                                                        Perícias:

          -**Corpo // Físico(140 + 20 + 30)**-                                 -**Perícias Específicas(140 + 70 + 30)**-

      Agilidade: 8 / 80 / 40                                               Medicina: 8 / 80 / 40
Constituição: 6/ 60 / 30                                                Cirurgia: 8 / 80/ 40
             Força: 5 / 50 / 25                                               Anatomia: 8 / 80 / 40

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

       -**Percepção // Ambiente(200 + 40 + 20)**-    -**Conhecimento // Experiências(200 + 80 + 10)**-

  Investigação: 9,5 / 95/ 47,5                                       Ciências: 9,5 / 95/ 47,5
           Escutar: 8,5 / 85/ 42,5                                  Tecnologia: 9,5 / 95 / 47,5
      Vigilância: 8,5 / 85/ 42,5                                   Linguagem: 9,5 / 95/ 47,5

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        -**Crime // Infiltração(110 + 10 + 20)**-                           -**Intelectual // Mental(110 + 50 + 20)**-

  Furtividade: 6 / 60/ 30                                                    Inteligência: 9 / 90 / 45
           Crime: 6 / 60 / 30                                                     Lábia: 6 / 60/ 30
    Distração: 2 / 20/ 10                                                     Psicologia: 3 / 30/ 15
"""

import re

import re

def extract_ficha_data(text: str) -> dict:
    data = {}

    # -------- Estado --------
    data["Nivel"] = int(re.search(r"Nível:\s*(\d+)", text).group(1))

    vida_match = re.search(r"Vida:\s*\((\d+)\)\s*//\s*\((\d+)\)", text)
    data["Vida"] = int(vida_match.group(1))
    data["Vida_Max"] = int(vida_match.group(2))

    san_match = re.search(r"Sanidade:\s*\((\d+)\)\s*//\s*\((\d+)\)", text)
    data["Sanidade"] = int(san_match.group(1))
    data["Sanidade_Max"] = int(san_match.group(2))

    data["Esforço"] = int(re.search(r"Esforço:\s*(\d+)", text).group(1))
    data["Armadura"] = int(re.search(r"Armadura:\s*(\d+)", text).group(1))

    arm_s_match = re.search(r"Armadura de sanidade:\s*(\d+)", text)
    data["Armadura_S"] = int(arm_s_match.group(1))

    # -------- Perícias --------
    # Capture all skill lines like:
    # Agilidade: 8 / 80 / 40
    skills = re.findall(
        r"([A-Za-zçÇãÃéÉíÍôÔúÚ]+):\s*([\d,]+)\s*/\s*([\d,]+)\s*/\s*([\d,]+)",
        text
    )

    # Convert decimal comma to float properly
    def parse_number(n):
        return float(n.replace(",", "."))

    for i, (name, n1, n2, n3) in enumerate(skills[:6], start=1):
        data[f"BP{i}_N"] = name
        data[f"BP{i}_V"] = parse_number(n1)
        data[f"BP{i}_P1_N"] = parse_number(n2)
        data[f"BP{i}_P1_V"] = None
        data[f"BP{i}_P2_N"] = parse_number(n3)
        data[f"BP{i}_P2_V"] = None
        data[f"BP{i}_P3_N"] = None
        data[f"BP{i}_P3_V"] = None

    return data


dados = extract_ficha_data(sheet)

print(f"Nivel: {dados['Nivel']}")
print(f"Vida: {dados['Vida']} {dados['Vida_Max']}")
print(f"Sanidade: {dados['Sanidade']} {dados['Sanidade_Max']}")
print(f"Esforço: {dados['Esforço']}")
print(f"Armadura: {dados['Armadura']}")
print(f"Armadura de sanidade: {dados['Armadura_S']}")

for i in range(1, 7):
    print(f"BP{i} - {dados[f'BP{i}_N']}: {dados[f'BP{i}_V']} / {dados[f'BP{i}_P1_N']} / {dados[f'BP{i}_P2_N']}")
    