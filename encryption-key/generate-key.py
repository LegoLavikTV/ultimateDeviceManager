import random
import string
import os
from cryptography.fernet import Fernet

def generate_key():
    parts = []

    # Part 1: Eight alphanumeric with at least two uppercase and two lowercase letters
    while True:
        part1 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if sum(c.isupper() for c in part1) >= 2 and sum(c.islower() for c in part1) >= 2:
            parts.append(part1)
            break

    # Part 2: Eight alphanumeric, ASCII sum divisible by 7, with at least two digits
    while True:
        part2 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if sum(c.isdigit() for c in part2) >= 2 and sum(ord(c) for c in part2) % 7 == 0:
            parts.append(part2)
            break

    # Part 3: At least two special characters and alphanumeric mix
    while True:
        part3 = ''.join(random.choices(string.ascii_letters + string.digits + "@#!$", k=8))
        if sum(c in "@#!$" for c in part3) >= 2:
            parts.append(part3)
            break

    # Part 4: Eight lowercase letters, starting and ending with the same letter
    while True:
        part4 = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase, k=6)) + random.choice(string.ascii_lowercase)
        if part4[0] == part4[-1]:
            parts.append(part4)
            break

    # Part 5: Eight alphanumeric, numeric portion divisible by 5
    while True:
        part5 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if int(''.join(filter(str.isdigit, part5)) or "0") % 5 == 0:
            parts.append(part5)
            break

    # Part 6: At least three uppercase letters
    while True:
        part6 = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if sum(c.isupper() for c in part6) >= 3:
            parts.append(part6)
            break

    # Part 7: At least one special character, the rest lowercase letters
    part7 = random.choice("@#!$") + ''.join(random.choices(string.ascii_lowercase, k=7))
    parts.append(part7)

    # Part 8: Only lowercase letters or digits
    part8 = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    parts.append(part8)

    # Part 9: Uppercase letters, ASCII sum divisible by 3
    while True:
        part9 = ''.join(random.choices(string.ascii_uppercase, k=8))
        if sum(ord(c) for c in part9) % 3 == 0:
            parts.append(part9)
            break

    # Part 10: Eight digits, sum of digits equals 30
    while True:
        part10_digits = [random.randint(0, 9) for _ in range(8)]
        if sum(part10_digits) == 30:
            part10 = ''.join(map(str, part10_digits))
            parts.append(part10)
            break

    # Join parts without dashes
    key = ''.join(parts)
    return key

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

with open("encryption_key.bin", "wb") as file:
    file.write(encryption_key)  # Save as bytes
with open("encrypted_key.bin", "wb") as file:
    file.write(key_encrypted)