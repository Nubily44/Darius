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

if __name__ == "__main__":
    
    # Example usage
    print(dice(6, 2))  # Roll a 6-sided die with advantage of 2
    print(dice(20, 3)) # Roll a 20-sided die with advantage of 3
