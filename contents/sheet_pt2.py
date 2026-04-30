sheet = """
------------------------------------------ Combate ------------------------------------------ ( ( Pt 2 ) )

                                                             Corpo a corpo (285):

              Combate Direto: 95

              Assalto: 95

(lvl>5) Artes Marciais: 10

(lvl>8) Duelo de Névoa: 85
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

                                                             Armas de Fogo (235):

             Armas de Fogo P: 90

             Armas de Fogo G: 70

(lvl>5) Armas de Fogo XL: 65

(lvl>7) Armas de Fogo Ocultistas: 10
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

                                                             Armas Brancas (335):

             Armas Brancas P: 95

             Armas Brancas G: 70

(lvl>4) Armas Brancas XL: 70

(lvl>7) Armas Brancas Ocultistas: 95
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


                           Correntes da Perdição - Presa
                    Dano normal:   4d4 + (0)
                    Dano bom:        5d4 + (0)
                    Dano extremo: 6d4 + 2(0)

                           Correntes da Perdição - Predador - só funciona se o alvo estiver imobilizado por 3 rodadas
                    Dano normal:   3d10 + 4d12 + (5~) + (5\*)
                    Dano bom:        7d12 + (5~) + (5\*)
                    Dano extremo: 8d12 + (15~) + (15\*)

                           Zirkani - Lâmina menor 
                    Dano normal:    (5~) + (5\*) + (5|) + (5-) + (5^)
                    Dano bom:         (10~) + (10\*) + (10|) + (10-) + (10^)
                    Dano extremo:  (20~) + (20\*) + (20|) + (20-) + (20^)


                           Zirkani - Lâmina maior
                    Dano normal:   5d12 + 45 + 4d20
                    Dano bom:        7d12 + 55 + 5d20
                    Dano extremo: 10d12 + 75 + 9d20

---------------------------------------------------------------------------------------------------
"""
import re

def extract_weapon_data(text: str) -> dict:
    data = {}

    damage_pattern = re.compile(r'Dano\s+(normal|bom|extremo):\s*(.+)')
    
    weapon_index = 0
    current_weapon = None

    damage_map = {
        "normal": "D1",
        "bom": "D2",
        "extremo": "D3"
    }

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        # Detect weapon name (line that is NOT damage and not separator)
        if (
            "Dano" not in stripped and
            not stripped.startswith("-") and
            not stripped.startswith("(")
        ):
            weapon_index += 1
            current_weapon = f"W{weapon_index}"
            data[f"{current_weapon}_N"] = stripped
            continue

        # Detect damage lines
        damage_match = damage_pattern.search(stripped)
        if damage_match and current_weapon:
            dmg_type = damage_match.group(1)
            dmg_value = damage_match.group(2).strip()

            key_suffix = damage_map[dmg_type]
            data[f"{current_weapon}_{key_suffix}"] = dmg_value

    return data

def main():
      di = extract_weapon_data(sheet)
      print(di)