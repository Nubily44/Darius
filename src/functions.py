import random

def dice(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    return random.randint(1, n)
