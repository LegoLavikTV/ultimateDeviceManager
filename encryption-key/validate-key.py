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

def validate_key(key):
    if len(key) != 80:
        print("Invalid key format: Should be exactly 80 characters long.")
        return False

    parts = [key[i:i+8] for i in range(0, 80, 8)]

    # Part 1 validation: At least two uppercase and two lowercase letters
    part1 = parts[0]
    if not re.match(r"^[A-Za-z0-9]{8}$", part1) or sum(c.isupper() for c in part1) < 2 or sum(c.islower() for c in part1) < 2:
        print("Part 1 failed:", part1)
        return False

    # Part 2 validation: ASCII sum divisible by 7 with at least two digits
    part2 = parts[1]
    if not re.match(r"^[A-Za-z0-9]{8}$", part2) or sum(c.isdigit() for c in part2) < 2 or sum(ord(c) for c in part2) % 7 != 0:
        print("Part 2 failed:", part2)
        return False

    # Part 3 validation: At least two special characters
    part3 = parts[2]
    if not re.match(r"^[A-Za-z0-9@#!$]{8}$", part3) or sum(c in "@#!$" for c in part3) < 2:
        print("Part 3 failed:", part3)
        return False

    # Part 4 validation: Eight lowercase letters, starts and ends the same
    part4 = parts[3]
    if not re.match(r"^[a-z]{8}$", part4) or part4[0] != part4[-1]:
        print("Part 4 failed:", part4)
        return False

    # Part 5 validation: Numeric portion divisible by 5
    part5 = parts[4]
    if not re.match(r"^[A-Za-z0-9]{8}$", part5) or int(''.join(filter(str.isdigit, part5)) or "0") % 5 != 0:
        print("Part 5 failed:", part5)
        return False

    # Part 6 validation: At least three uppercase letters
    part6 = parts[5]
    if not re.match(r"^[A-Za-z0-9]{8}$", part6) or sum(c.isupper() for c in part6) < 3:
        print("Part 6 failed:", part6)
        return False

    # Part 7 validation: One special character and lowercase letters
    part7 = parts[6]
    if not re.match(r"^[a-z@#!$]{8}$", part7) or sum(c in "@#!$" for c in part7) != 1:
        print("Part 7 failed:", part7)
        return False

    # Part 8 validation: Only lowercase letters or digits
    part8 = parts[7]
    if not re.match(r"^[a-z0-9]{8}$", part8):
        print("Part 8 failed:", part8)
        return False

    # Part 9 validation: Uppercase ASCII sum divisible by 3
    part9 = parts[8]
    if not re.match(r"^[A-Z]{8}$", part9) or sum(ord(c) for c in part9) % 3 != 0:
        print("Part 9 failed:", part9)
        return False

    # Part 10 validation: Eight digits, sum of digits equals 30
    part10 = parts[9]
    if not re.match(r"^\d{8}$", part10) or sum(int(c) for c in part10) != 30:
        print("Part 10 failed:", part10)
        return False
    return True

print("Is the key valid:", validate_key(check_key))
def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
remove_file(encryption_key_file)
remove_file(encrypted_key_file)
