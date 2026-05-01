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
"""
BPC1_N
BPC1_V
BPC1_P1_N
BPC1_P1_V
BPC1_P2_N
BPC1_P2_V
BPC1_P3_N
BPC1_P3_V
BPC2_N
BPC2_V
BPC2_P1_N
BPC2_P1_V
BPC2_P2_N
BPC2_P2_V
BPC2_P3_N
BPC2_P3_V
BPC3_N
BPC3_V
BPC3_P1_N
BPC3_P1_V
BPC3_P2_N
BPC3_P2_V
BPC3_P3_N
BPC3_P3_V
W1_N
W1_D1
W1_D2
W1_D3
W2_N
W2_D1
W2_D2
W2_D3
W3_N
W3_D1
W3_D2
W3_D3
W4_N
W4_D1
W4_D2
W4_D3
"""
import re

import warnings


import re

def parse_sheet(sheet: str):
    result = {}

    lines = sheet.splitlines()

    bp_index = 0
    skill_index = 0
    weapon_index = 0

    current_bp = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # -------------------------
        # 1. BLOCO PERÍCIA
        # -------------------------
        bp_match = re.match(r'(.+?)\s*\((\d+)\):', line)
        if bp_match:
            bp_index += 1
            skill_index = 0

            name = bp_match.group(1).strip()
            value = int(bp_match.group(2))

            result[f"BPC{bp_index}_N"] = name
            result[f"BPC{bp_index}_V"] = value

            current_bp = bp_index
            i += 1
            continue

        # -------------------------
        # 2. PERÍCIAS
        # -------------------------
        skill_match = re.match(r'(?:\(lvl>\d+\)\s*)?(.+?):\s*(\d+)', line)
        if skill_match and current_bp is not None:
            skill_index += 1

            name = skill_match.group(1).strip()
            value = int(skill_match.group(2))

            result[f"BPC{current_bp}_P{skill_index}_N"] = name
            result[f"BPC{current_bp}_P{skill_index}_V"] = value

            i += 1
            continue

        # -------------------------
        # 3. WEAPONS
        # -------------------------
        if "Dano normal:" in line:
            # weapon name is previous non-empty line
            j = i - 1
            while j >= 0 and not lines[j].strip():
                j -= 1

            weapon_name = lines[j].strip()

            d1 = line.split("Dano normal:")[1].strip()
            d2 = lines[i+1].split("Dano bom:")[1].strip()
            d3 = lines[i+2].split("Dano extremo:")[1].strip()

            weapon_index += 1

            result[f"W{weapon_index}_N"] = weapon_name
            result[f"W{weapon_index}_D1"] = d1
            result[f"W{weapon_index}_D2"] = d2
            result[f"W{weapon_index}_D3"] = d3

            i += 3
            continue

        i += 1

    return result

def main():
    warnings.filterwarnings("ignore", category=SyntaxWarning)
    di = parse_sheet(sheet)
    for k, v in di.items():
        print(k, "=", v)
        
main()