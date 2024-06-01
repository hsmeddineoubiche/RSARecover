import argparse
import concurrent.futures
from Crypto.Util.number import inverse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dixon_factorization import dixon_factorize
from pollards_p1 import pollards_p1_factorize
from wiener_attack import wiener_attack

banner = """
    ____  _____  ___     ____                                      
   / __ \/ ___/ /   |   / __ \ ___   _____ ____  _   __ ___   _____
  / /_/ /\__ \ / /| |  / /_/ // _ \ / ___// __ \| | / // _ \ / ___/
 / _, _/___/ // ___ | / _, _//  __// /__ / /_/ /| |/ //  __// /    
/_/ |_|/____//_/  |_|/_/ |_| \___/ \___/ \____/ |___/ \___//_/     
                                                                    
"""

print(banner,"\n")


def load_public_key(public_key_pem):
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )
    return public_key

def generate_rsa_private_key_pem(d, p, q, e, n):
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_numbers = rsa.RSAPrivateNumbers(
        p=p,
        q=q,
        d=d,
        dmp1=d % (p - 1),
        dmq1=d % (q - 1),
        iqmp=inverse(q, p),
        public_numbers=rsa.RSAPublicNumbers(e, n)
    )
    private_key = private_numbers.private_key(default_backend())

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode('utf-8')

def try_factorization_method(method, args, timeout):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(method, *args)
        try:
            p, q = future.result(timeout=timeout)
            return p, q
        except concurrent.futures.TimeoutError:
            print(f"{method.__name__} timed out")
            return None
        except Exception as ex:
            print(f"{method.__name__} failed: {ex}")
            return None

def try_factorization_methods(n, e, B, timeout):
    methods = [
        ("Dixon's Factorization", dixon_factorize, (n,)),
        ("Wiener's Attack", wiener_attack, (n, e)),
        ("Pollard's p-1 Method", pollards_p1_factorize, (n, B)),
    ]

    for name, method, args in methods:
        result = try_factorization_method(method, args, timeout)
        if result:
            print(f"Success with {name}")
            return result

    raise ValueError("All factorization methods failed")

def main():
    parser = argparse.ArgumentParser(description="RSA Private Key Recovery Tool")
    parser.add_argument("public_key_file", help="Path to the public key PEM file")
    parser.add_argument("--method", choices=["dixon", "pollard", "wiener"], help="Factorization method to use")
    parser.add_argument("--B", type=int, default=1000000, help="Bound for Pollard's p-1 method")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout for each factorization method in seconds")
    
    args = parser.parse_args()

    with open(args.public_key_file, "r") as f:
        public_key_pem = f.read()

    public_key = load_public_key(public_key_pem)
    n = public_key.public_numbers().n
    e = public_key.public_numbers().e

    if args.method:
        method_mapping = {
            "dixon": (dixon_factorize, (n,)),
            "pollard": (pollards_p1_factorize, (n, args.B)),
            "wiener": (wiener_attack, (n, e)),
        }
        method, method_args = method_mapping[args.method]
        result = try_factorization_method(method, method_args, args.timeout)
        if not result:
            return
        p, q = result
    else:
        try:
            p, q = try_factorization_methods(n, e, args.B, args.timeout)
        except ValueError as ex:
            print(ex)
            return

    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

    private_key_pem = generate_rsa_private_key_pem(d, p, q, e, n)
    print(private_key_pem)

if __name__ == "__main__":
    main()
