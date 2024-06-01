from math import gcd, isqrt
from sympy import nextprime
import bitarray

def primes(n):
    prime_lst = []
    p = 2
    while len(prime_lst) < n:
        if all(p % prime != 0 for prime in prime_lst):
            prime_lst.append(p)
        p += 1
    return prime_lst

def powmod(x, y, z):
    res = 1
    x = x % z
    while y > 0:
        if y % 2 == 1:
            res = (res * x) % z
        y = y // 2
        x = (x * x) % z
    return res

def _powmod_base_list(base_lst, exp, mod):
    return list(powmod(i, exp, mod) for i in base_lst)

def dixon_factorize(N, B=7):
    base = primes(B)
    lqbf = pow(base[-1], 2) + 1
    QBF = bitarray.bitarray(lqbf)  

    basej2N = _powmod_base_list(base, 2, N)
    for p in basej2N: QBF[p] = 1

    for i in range(isqrt(N), N):
        i2N = powmod(i, 2, N)
        if i2N < lqbf and QBF[i2N] == 1:
            for k in range(0, len(base)):
                if QBF[basej2N[k]] == 1 and 1 < (f := gcd(i - base[k], N)) < N:
                    return f, N // f
    raise ValueError("Dixon's method failed to factorize the number")

