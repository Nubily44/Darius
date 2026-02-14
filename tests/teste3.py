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

def extract_ficha_data(text: str) -> dict:
    data = {}

    # ---------- Estado ----------
    data["Nivel"] = int(re.search(r"Nível:\s*(\d+)", text).group(1))

    vida_atual, vida_max = re.search(
        r"Vida:\s*\((\d+)\)\s*//\s*\((\d+)\)", text
    ).groups()
    data["Vida"] = int(vida_atual)
    data["Vida_Max"] = int(vida_max)

    san_atual, san_max = re.search(
        r"Sanidade:\s*\((\d+)\)\s*//\s*\((\d+)\)", text
    ).groups()
    data["Sanidade"] = int(san_atual)
    data["Sanidade_Max"] = int(san_max)

    data["Esforço"] = int(re.search(r"Esforço:\s*(\d+)", text).group(1))
    data["Armadura"] = int(re.search(r"Armadura:\s*(\d+)", text).group(1))

    arm_s_match = re.search(r"Armadura de sanidade:\s*(\d+)", text)
    data["Armadura_S"] = int(arm_s_match.group(1)) if arm_s_match else 0

    # ---------- Skill extraction ----------
    skill_pattern = re.compile(
        r"([\wÀ-ÿ]+):\s*([\d,]+)\s*/\s*([\d,]+)\s*/\s*([\d,]+)"
    )

    skills = skill_pattern.findall(text)

    def to_float(v):
        return float(v.replace(",", "."))

    # Blocks definition (fixed order)
    blocks = [
        "BP1", "BP2", "BP3", "BP4", "BP5", "BP6"
    ]

    skill_index = 0

    for block in blocks:
        data[f"{block}_N"] = block
        data[f"{block}_V"] = 3  # each block has 3 skills

        for i in range(1, 4):
            name, v1, v2, v3 = skills[skill_index]

            data[f"{block}_P{i}_N"] = name
            data[f"{block}_P{i}_V"] = to_float(v2)

            skill_index += 1

    return data


dados = sheet

print(dados["Vida"], dados["BP4_P2_N"], dados["BP4_P2_V"])