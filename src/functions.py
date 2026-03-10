import sys
import random
import time
import pandas as pd
import re

def dice(n: int, advantage: int = 1) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    
    dices = []
    
    for _ in range(advantage):
        dices.append(random.randint(1, n))
        print(f"     [ROLLS] | d{n}: {dices[-1]}")
    return min(dices)

def rolagem_sum(n: int, advantage: int = 1) -> int:
    
    if n < 1:
        raise ValueError("n must be >= 1")
    
    dices = []
    
    for _ in range(advantage):
        dices.append(random.randint(1, n))
        print(f"     [ROLLS] | d{n}: {dices[-1]}")
    return sum(dices)

def rolagem_expressao(expressao: str) -> int:
    expressao = expressao.replace(" ", "")
    
    # Split keeping + and -
    tokens = re.findall(r'[+-]?[^+-]+', expressao)
    
    total = 0
    
    for token in tokens:
        sinal = 1
        
        if token.startswith("+"):
            token = token[1:]
        elif token.startswith("-"):
            sinal = -1
            token = token[1:]
        
        if "d" in token.lower():
            # Dice case
            partes = token.lower().split("d")
            
            qtd = int(partes[0]) if partes[0] != "" else 1
            lados = int(partes[1])
            resultado = rolagem_sum(lados, qtd)
            total += sinal * resultado
        else:
            # Flat number
            total += sinal * int(token)
    return total

def Wrapper(func):
    def wrapper(*args, **kwargs):
        arg_list = []
        
        # Prepare argument list
        for name, value in zip(func.__code__.co_varnames, args):
            if isinstance(value, pd.DataFrame):
                arg_list.append(f"{name}: DataFrame ({value.shape})")
            else:
                arg_list.append(f"{name}: {value}")
        for k, v in kwargs.items():
            if isinstance(v, pd.DataFrame):
                arg_list.append(f"{k}: DataFrame ({v.shape})")
            else:
                arg_list.append(f"{k}: {v}")

        #print(f"Executando <{func.__name__}>\n({'\n'.join(arg_list)})\n")

        # Measure execution time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        #print(f"Tempo de execução: {end - start:.6f} segundos\n")
        return result
    return wrapper

class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

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
        data[f"BP{i+1}_V"] = int(sum(nums))

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
            data[f"BP{left_block}_P{p}_V"] = int(max(values))
            skill_index += 1

            # Right column skill
            name, v1, v2, v3 = skills[skill_index]
            values = [float(v.replace(",", ".")) for v in (v1, v2, v3)]
            data[f"BP{right_block}_P{p}_N"] = name.strip()
            data[f"BP{right_block}_P{p}_V"] = int(max(values))
            skill_index += 1

    sorted_data = sort_ficha_dict(data)
    return sorted_data

def update_state(var: str, value: str, file_path: str = "src/state.log") -> None:
    lines = []
    found = False

    with open(file_path, "r", encoding='utf-8') as f:
        for line in f:
            if "=" in line:
                name, current = line.split("=", 1)
                name = name.strip()

                if name == var:
                    lines.append(f"{var} = {value}\n")
                    found = True
                else:
                    lines.append(line)
            else:
                lines.append(line)

    if not found:
        lines.append(f"{var} = {value}\n")

    with open(file_path, "w", encoding='utf-8') as f:
        f.writelines(lines)

def update_variable(var: str, value, file_path: str):
    lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith(var):
                lines.append(f"{var} = {repr(value)}\n")
            else:
                print("AAAAAAA", line.strip(), var)
                lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

import ast

def read_state(file_path: str = "src/state.log") -> dict:
    state = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                var, value = line.split("=", 1)
                var = var.strip()
                value = value.strip()

                try:
                    state[var] = ast.literal_eval(value)
                except Exception:
                    state[var] = value  # fallback if it isn't a valid literal

    return state

if __name__ == "__main__":
    
    # Example usage
    #print(dice(6, 2))  # Roll a 6-sided die with advantage of 2
    #print(dice(20, 3)) # Roll a 20-sided die with advantage of 3
    
    print(rolagem_expressao("2d6 + 3 - 1d4"))  # Roll 2d6, add 3, subtract 1d4
    update_state("Vida_Max", "100")