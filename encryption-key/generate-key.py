import random
import string
import os
from cryptography.fernet import Fernet

def generate_part(criteria):
    while True:
        part = ''.join(random.choices(criteria['chars'], k=8))
        if criteria['validation'](part):
            return part
def generate_key():
    criteria = {
        'part1': {
            'chars': string.ascii_letters + string.digits,
            'validation': lambda p: sum(c.isupper() for c in p) >= 2 and sum(c.islower() for c in p) >= 2
        },
        'part2': {
            'chars': string.ascii_letters + string.digits,
            'validation': lambda p: sum(c.isdigit() for c in p) >= 2 and sum(ord(c) for c in p) % 7 == 0
        },
        'part3': {
            'chars': string.ascii_letters + string.digits + "@#!$",
            'validation': lambda p: sum(c in "@#!$" for c in p) >= 2
        },
        'part4': {
            'chars': string.ascii_lowercase,
            'validation': lambda p: p[0] == p[-1]
        },
        'part5': {
            'chars': string.ascii_letters + string.digits,
            'validation': lambda p: int(''.join(filter(str.isdigit, p)) or "0") % 5 == 0
        },
        'part6': {
            'chars': string.ascii_letters + string.digits,
            'validation': lambda p: sum(c.isupper() for c in p) >= 3
        },
        'part7': {
            'chars': string.ascii_lowercase + "@#!$",
            'validation': lambda p: sum(c in "@#!$" for c in p) == 1
        },
        'part8': {
            'chars': string.ascii_lowercase + string.digits,
            'validation': lambda p: True  # Always valid
        },
        'part9': {
            'chars': string.ascii_uppercase,
            'validation': lambda p: sum(ord(c) for c in p) % 3 == 0
        },
        'part10': {
            'chars': '01234567',  # Digits only, but control sum needs to be handled
            'validation': lambda p: sum(int(c) for c in p) == 30
        }
    }
    parts = []
    for part_name in criteria.keys():
        if part_name == 'part10':
            while True:
                part10_digits = [random.randint(0, 9) for _ in range(8)]
                if sum(part10_digits) == 30:
                    parts.append(''.join(map(str, part10_digits)))
                    break
        else:
            parts.append(generate_part(criteria[part_name]))
    return ''.join(parts)

# Generate the key
generated_key = generate_key()

encryption_key_file = "encryption_key.bin"
encrypted_key_file = "encrypted_key.bin"
def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
remove_file(encryption_key_file)
remove_file(encrypted_key_file)

encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)
key_bytes = generated_key.encode('utf-8')
key_encrypted = cipher_suite.encrypt(key_bytes)

with open(encryption_key_file, "wb") as file:
    file.write(encryption_key)  # Save as bytes
with open(encrypted_key_file, "wb") as file:
    file.write(key_encrypted)