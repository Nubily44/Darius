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

def extract_ficha_data(sheet: str) -> dict:
    data = {}

    # ---------- Estado ----------
    data["Nivel"] = int(re.search(r"Nível:\s*(\d+)", sheet).group(1))

    vida = re.search(r"Vida:\s*\((\d+)\)\s*//\s*\((\d+)\)", sheet)
    data["Vida"] = int(vida.group(1))
    data["Vida_Max"] = int(vida.group(2))

    sanidade = re.search(r"Sanidade:\s*\((\d+)\)\s*//\s*\((\d+)\)", sheet)
    data["Sanidade"] = int(sanidade.group(1))
    data["Sanidade_Max"] = int(sanidade.group(2))

    data["Esforço"] = int(re.search(r"Esforço:\s*(\d+)", sheet).group(1))
    data["Armadura"] = int(re.search(r"Armadura:\s*(\d+)", sheet).group(1))
    data["Armadura_S"] = int(re.search(r"Armadura de sanidade:\s*(\d+)", sheet).group(1))

    # ---------- Blocks ----------
    block_pattern = r"-\*\*(.*?)\((.*?)\)\*\*-"
    blocks = re.findall(block_pattern, sheet)

    for i, (name, values) in enumerate(blocks):
        nums = [
            float(x.strip().replace(",", "."))
            for x in values.split("+")
        ]
        data[f"BP{i+1}_N"] = name.strip()
        data[f"BP{i+1}_V"] = max(nums)

    # ---------- Skills ----------
    skill_pattern = r"([A-Za-zÀ-ÿçÇãõéíúêôÁÉÍÓÚÊÔÃÕ]+):\s*([\d,\.]+)\s*/\s*([\d,\.]+)\s*/\s*([\d,\.]+)"
    skills = re.findall(skill_pattern, sheet)

    # Assign vertically (pairs of blocks)
    skill_index = 0
    for pair_start in range(0, 6, 2):  # (0-1), (2-3), (4-5)
        left_block = pair_start + 1
        right_block = pair_start + 2

        for p in range(1, 4):  # 3 skills each
            # Left column skill
            name, v1, v2, v3 = skills[skill_index]
            values = [float(v.replace(",", ".")) for v in (v1, v2, v3)]
            data[f"BP{left_block}_P{p}_N"] = name.strip()
            data[f"BP{left_block}_P{p}_V"] = max(values)
            skill_index += 1

            # Right column skill
            name, v1, v2, v3 = skills[skill_index]
            values = [float(v.replace(",", ".")) for v in (v1, v2, v3)]
            data[f"BP{right_block}_P{p}_N"] = name.strip()
            data[f"BP{right_block}_P{p}_V"] = max(values)
            skill_index += 1

    return data

def sort_ficha_dict(data: dict) -> dict:
    def sort_key(key):
        # Estado fields first
        estado_order = [
            "Nivel", "Vida", "Vida_Max",
            "Sanidade", "Sanidade_Max",
            "Esforço", "Armadura", "Armadura_S"
        ]

        if key in estado_order:
            return (0, estado_order.index(key))

        # Match BP structure
        match = re.match(r"BP(\d+)(?:_P(\d+))?_(N|V)", key)
        if match:
            bp = int(match.group(1))
            p = match.group(2)
            nv = match.group(3)

            # Block name/value first
            if p is None:
                return (1, bp, 0, 0 if nv == "N" else 1)

            # Then skills ordered
            return (1, bp, int(p), 0 if nv == "N" else 1)

        # Fallback
        return (2, key)

    sorted_keys = sorted(data.keys(), key=sort_key)
    return {k: data[k] for k in sorted_keys}

dados = extract_ficha_data(sheet)
dados_sort = sort_ficha_dict(dados)
for k, v in dados_sort.items():
    print(k, ":", v)
