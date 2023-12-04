import random
import sympy
import argparse
import time

class BBS:
    def __init__(self, seed=3, p=11, q=23):
        self.seed = seed
        self.p = p
        self.q = q
        self.M = p * q
        self.x_n = seed

    def _get_number_of_1_bits(self, bits):
        # Returns the number of 1-valued bits in the integer-encoded BITS
        return bin(bits).count('1')

    def _get_even_parity_bit(self, bits):
        # Returns the even parity bit of the integer-encoded BITS
        return self._get_number_of_1_bits(bits) % 2

    def _get_least_significant_bit(self, bits):
        # Returns the least significant bit of the integer-encoded BITS
        return bits & 1

    def _next(self):
        # Generate the next value in the Blum-Blum-Shub sequence
        x_n_plus_1 = (self.x_n ** 2) % self.M
        even_parity_bit = self._get_even_parity_bit(x_n_plus_1)
        least_significant_bit = self._get_least_significant_bit(x_n_plus_1)
        self.x_n = x_n_plus_1
        return x_n_plus_1, even_parity_bit, least_significant_bit

    def generate_sequence(self, length, method="least_significant_bit"):
        # Generate a sequence of pseudorandom numbers
        if method == "least_significant_bit":
            sequence = [self._next()[2] for _ in range(length)]
        elif method == "even_parity_bit":
            sequence = [self._next()[1] for _ in range(length)]
        else:
            sequence = [self._next()[0] for _ in range(length)]
        return sequence

class LCG:
    def __init__(self, seed, a, c, m):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def _next(self):
        # Internal method to calculate the next state in the LCG
        self.state = (self.a * self.state + self.c) % self.m
        return self.state % 128

    def generate_sequence(self, length):
        # Generate a sequence of pseudorandom numbers
        sequence = [self._next() for _ in range(length)]
        return sequence

class StreamCipher:
    def __init__(self, key):
        self.key = key
        self.key_length = len(key)

        # lcg generation
        lcg_seed = random.randint(0, 2 ** 32 - 1)
        lcg_a = random.randint(1, 2 ** 16 - 1)
        lcg_c = random.randint(0, 2 ** 16 - 1)
        lcg_m = random.randint(2 ** 16, 2 ** 32 - 1)
        self.lcg = LCG(lcg_seed, lcg_a, lcg_c, lcg_m)

        # lcg generation
        bbs_seed = random.randint(2, 2 ** 32 - 1)
        bbs_p = sympy.randprime(2 ** 16, 2 ** 32 - 1)
        bbs_q = sympy.randprime(2 ** 16, 2 ** 32 - 1)
        while bbs_p % 4 != 3 or bbs_q % 4 != 3:
            bbs_p = sympy.randprime(2 ** 16, 2 ** 32 - 1)
            bbs_q = sympy.randprime(2 ** 16, 2 ** 32 - 1)
        self.bbs = BBS(bbs_seed, bbs_p, bbs_q)

        # Generate keystreams once during initialization
        self.keystream_bbs = self._generate_keystream(len(key), method="BBS")
        self.keystream_lcg = self._generate_keystream(len(key), method="LCG")

    def _generate_keystream(self, length, method="BBS"):
        # Internal method to generate keystream based on the LCG and BBS
        if method == "BBS":
            return self.bbs.generate_sequence(length)
        return self.lcg.generate_sequence(length)

    def encrypt(self, plaintext, method="BBS"):
        # Encrypt the plaintext using XOR with the pre-generated keystream
        ciphertext = [ord(plaintext[i]) ^ self.keystream_bbs[i] if method == "BBS" else
                      ord(plaintext[i]) ^ self.keystream_lcg[i] for i in range(len(plaintext))]
        return ''.join(chr(c) for c in ciphertext)

    def decrypt(self, ciphertext, method="BBS"):
        # Decrypt the ciphertext using XOR with the pre-generated keystream
        plaintext = [chr(ord(ciphertext[i]) ^ self.keystream_bbs[i] if method == "BBS" else
                        ord(ciphertext[i]) ^ self.keystream_lcg[i]) for i in range(len(ciphertext))]
        return ''.join(plaintext)


def main():
    parser = argparse.ArgumentParser(description='A simple Stream Cipher CLI script.')
    parser.add_argument('--key', help='key used in stream cipher', required=True)
    parser.add_argument('--plaintext', help='plaintext to encrypt', default="Hello, Stream Cipher!")

    args = parser.parse_args()

    key = args.key
    plaintext = args.plaintext

    key = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]

    # Create a StreamCipher object with the key
    stream_cipher = StreamCipher(key)

    # Encrypt the plaintext
    encrypted_text_bbs = stream_cipher.encrypt(plaintext, method="BBS")
    print(f"Encrypted BBS: {encrypted_text_bbs}")
    print(f"BBS Encryption Time: {2}")

    encrypted_text_lcg = stream_cipher.encrypt(plaintext, method="LCG")
    print(f"Encrypted LCG: {encrypted_text_lcg}")
    print(f"LCG Encryption Time: {2}")

    # Decrypt the ciphertext
    decrypted_text_bbs = stream_cipher.decrypt(encrypted_text_bbs, method="BBS")
    print(f"Decrypted BBS: {decrypted_text_bbs}")
    print(f"BBS Decryption Time: {2}")

    decrypted_text_lcg = stream_cipher.decrypt(encrypted_text_lcg, method="LCG")
    print(f"Decrypted LCG: {decrypted_text_lcg}")
    print(f"LCG Decryption Time: {2}")

if __name__ == "__main__":
    bbs = BBS()
    nums = bbs.generate_sequence(30, "raw")
    print(nums)
