import random

def dice(n: int, advantage: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    return max(random.randint(1, n) for _ in range(advantage))
