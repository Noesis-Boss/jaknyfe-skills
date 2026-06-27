import math


def is_prime(n: int) -> bool:
    """Check if a number is prime using trial division up to sqrt(n)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    primes = [n for n in range(1, 101) if is_prime(n)]
    print(primes)
