# RSARecover

## Overview
The RSA Private Key Recovery Tool is a command-line utility designed to assist in the recovery of RSA private keys when only the public key is available. It implements various factorization methods and attacks to deduce the prime factors of the modulus, which are essential for reconstructing the private key.

## Features
- Supports multiple factorization methods, including Dixon's Factorization, Pollard's p-1 Method, and Wiener's Attack.
- User-friendly command-line interface with options to specify the factorization method, timeout, and other parameters.
- Utilizes concurrent execution to speed up the factorization process, leveraging the power of multiprocessing and multithreading.
- Generates the RSA private key in PEM format once the prime factors are successfully recovered, allowing smooth integration with other cryptographic tools and libraries.

Note that the tool has some issues with the timeout flag it's recommended to use the attack flag since the tool contains only three methods for now 

## Installation
Clone the repository and install the required dependencies:
```bash
git clone <repository_url>
cd <repository_directory>
pip install -r requirements.txt
```

## Usage
python main.py <public_key_file> [--method <method>] [--B <bound>] [--timeout <timeout>]

## Example
python3 main.py public_key --method wiener

