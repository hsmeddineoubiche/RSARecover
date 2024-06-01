from sympy import isprime, sqrt, Rational
from sympy.ntheory import continued_fraction_convergents
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from sympy.ntheory.modular import solve_congruence
from sympy.core.numbers import igcd

def fdivmod(a, b):
    return divmod(a, b)

def is_square(n):
    if n < 0:
        return False
    root = int(sqrt(n))
    return n == root * root

def trivial_factorization_with_n_phi(n, phi):
    a = (n - phi + 1) // 2
    b_squared = a * a - n
    if b_squared >= 0 and is_square(b_squared):
        b = int(sqrt(b_squared))
        p = a - b
        q = a + b
        if p * q == n:
            return p, q
    return None

def convergents_from_contfrac(frac):
    return list(continued_fraction_convergents(frac))

def rational_to_contfrac(x, y):
    a = x // y
    pquotients = [a]
    while y:
        x, y = y, x % y
        if y:
            a = x // y
            pquotients.append(a)
    return pquotients

def wiener_attack(n, e):
    convergents = convergents_from_contfrac(rational_to_contfrac(e, n))

    for k_d in convergents:
        k, d = k_d.p, k_d.q
        if k != 0:
            phi, q = fdivmod((e * d) - 1, k)
            if (phi & 1 == 0) and (q == 0):
                s = n - phi + 1
                discr = (s * s) - (n << 2)
                if discr > 0 and is_square(discr):
                    t = int(sqrt(discr))
                    if (s + t) & 1 == 0:
                        pq = trivial_factorization_with_n_phi(n, phi)
                        if pq is not None:
                            return pq
    raise ValueError("Wiener's method failed to factorize the number")

