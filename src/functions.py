import random

def random_between_1_and_n(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    return random.randint(1, n)
