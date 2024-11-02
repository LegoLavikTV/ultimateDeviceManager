import re
import os
from cryptography.fernet import Fernet

encryption_key_file = "encryption_key.bin"
encrypted_key_file = "encrypted_key.bin"

with open(encryption_key_file, "rb") as file:
    encryption_key = file.read().decode()
cipher_suite = Fernet(encryption_key)
with open(encrypted_key_file, "rb") as file:
    key_encrypted = file.read()

key_decrypted = cipher_suite.decrypt(key_encrypted)
check_key = key_decrypted.decode('utf-8')

def validate_part(part, checks):
    """Helper function to validate a single part against a set of checks."""
    for check in checks:
        if not check(part):
            return False
    return True
def validate_key(key):
    if len(key) != 80:
        print("Invalid key format: Should be exactly 80 characters long.")
        return False
    parts = [key[i:i + 8] for i in range(0, 80, 8)]
    validation_checks = [
        # Part 1 checks: At least two uppercase and two lowercase letters
        lambda p: re.match(r"^[A-Za-z0-9]{8}$", p) and sum(c.isupper() for c in p) >= 2 and sum(c.islower() for c in p) >= 2,
        # Part 2 checks: ASCII sum divisible by 7 with at least two digits
        lambda p: re.match(r"^[A-Za-z0-9]{8}$", p) and sum(c.isdigit() for c in p) >= 2 and sum(ord(c) for c in p) % 7 == 0,
        # Part 3 checks: At least two special characters
        lambda p: re.match(r"^[A-Za-z0-9@#!$]{8}$", p) and sum(c in "@#!$" for c in p) >= 2,
        # Part 4 checks: Eight lowercase letters, starts and ends the same
        lambda p: re.match(r"^[a-z]{8}$", p) and p[0] == p[-1],
        # Part 5 checks: Numeric portion divisible by 5
        lambda p: re.match(r"^[A-Za-z0-9]{8}$", p) and int(''.join(filter(str.isdigit, p)) or "0") % 5 == 0,
        # Part 6 checks: At least three uppercase letters
        lambda p: re.match(r"^[A-Za-z0-9]{8}$", p) and sum(c.isupper() for c in p) >= 3,
        # Part 7 checks: One special character and lowercase letters
        lambda p: re.match(r"^[a-z@#!$]{8}$", p) and sum(c in "@#!$" for c in p) == 1,
        # Part 8 checks: Only lowercase letters or digits
        lambda p: re.match(r"^[a-z0-9]{8}$", p),
        # Part 9 checks: Uppercase ASCII sum divisible by 3
        lambda p: re.match(r"^[A-Z]{8}$", p) and sum(ord(c) for c in p) % 3 == 0,
        # Part 10 checks: Eight digits, sum of digits equals 30
        lambda p: re.match(r"^\d{8}$", p) and sum(int(c) for c in p) == 30,
    ]
    for i, (part, checks) in enumerate(zip(parts, validation_checks)):
        if not validate_part(part, [checks]):
            print(f"Part {i + 1} failed:", part)
            return False
    return True
print("Is the key valid:", validate_key(check_key))
def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
remove_file(encryption_key_file)
remove_file(encrypted_key_file)