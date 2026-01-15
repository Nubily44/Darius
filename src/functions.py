import random

def dice(n: int, advantage: int = 1) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    
    dices = []
    
    for _ in range(advantage):
        dices.append(random.randint(1, n))
        print(f"d{n}: {dices[-1]}")
    return min(dices)


if __name__ == "__main__":
    
    # Example usage
    print(dice(6, 2))  # Roll a 6-sided die with advantage of 2
    print(dice(20, 3)) # Roll a 20-sided die with advantage of 3
