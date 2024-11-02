import random
import string
import os
from cryptography.fernet import Fernet

def generate_part1():
    while True:
        part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if sum(c.isupper() for c in part) >= 2 and sum(c.islower() for c in part) >= 2:
            return part
def generate_part2():
    while True:
        part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if sum(c.isdigit() for c in part) >= 2 and sum(ord(c) for c in part) % 7 == 0:
            return part
def generate_part3():
    while True:
        part = ''.join(random.choices(string.ascii_letters + string.digits + "@#!$", k=8))
        if sum(c in "@#!$" for c in part) >= 2:
            return part
def generate_part4():
    while True:
        part = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase, k=6)) + random.choice(string.ascii_lowercase)
        if part[0] == part[-1]:
            return part
def generate_part5():
    while True:
        part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if int(''.join(filter(str.isdigit, part)) or "0") % 5 == 0:
            return part
def generate_part6():
    while True:
        part = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if sum(c.isupper() for c in part) >= 3:
            return part
def generate_part7():
    return random.choice("@#!$") + ''.join(random.choices(string.ascii_lowercase, k=7))
def generate_part8():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
def generate_part9():
    while True:
        part = ''.join(random.choices(string.ascii_uppercase, k=8))
        if sum(ord(c) for c in part) % 3 == 0:
            return part
def generate_part10():
    while True:
        part10_digits = [random.randint(0, 9) for _ in range(8)]
        if sum(part10_digits) == 30:
            return ''.join(map(str, part10_digits))
def generate_key():
    parts = [
        generate_part1(),
        generate_part2(),
        generate_part3(),
        generate_part4(),
        generate_part5(),
        generate_part6(),
        generate_part7(),
        generate_part8(),
        generate_part9(),
        generate_part10(),
    ]
    return ''.join(parts)

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