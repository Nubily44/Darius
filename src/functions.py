import random
import time
import pandas as pd

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

if __name__ == "__main__":
    
    # Example usage
    print(dice(6, 2))  # Roll a 6-sided die with advantage of 2
    print(dice(20, 3)) # Roll a 20-sided die with advantage of 3
