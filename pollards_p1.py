import math
from sympy import gcd
from Crypto.Util.number import inverse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def pollards_p1(n, B=1000000):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
        d = gcd(a-1, n)
        if 1 < d < n:
            return int(d)  # Ensure d is a standard Python integer
    return None

def pollards_p1_factorize(n, B=1000000):
    p = pollards_p1(n, B)
    if not p:
        raise ValueError("Failed to find a factor using Pollard's p-1 method")
    q = n // p
    if p * q != n:
        raise ValueError("Failed to factorize n correctly")
    return p, q

