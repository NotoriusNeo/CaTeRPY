import argparse
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from pathlib import Path
import bcrypt

def encrypt_folder(input, output, password, salt_file):
    if not os.path.exists(input):
        print("Error: Folder to encrypt does not exist. Please provide a valid folder path.")
        return
    if not os.path.exists(output):
        os.makedirs(output)
    
    salt = bcrypt.gensalt()
    if salt_file:
        with open(salt_file, 'wb') as f:
            f.write(salt)
    elif salt_file is not None:
        with open(salt_file, 'wb') as f:
            f.write(salt)
    
    key = bcrypt.kdf(password=password.encode(), salt=salt, desired_key_bytes=16, rounds=100)

    for root, dirs, files in os.walk(input):
        for file in files:
            iv = get_random_bytes(8) 
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, input)
            encrypted_file_path = os.path.join(output, relative_path)
            Path(encrypted_file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "rb") as f:
                plaintext = f.read()

            cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
            ciphertext = cipher.encrypt(plaintext)

            with open(encrypted_file_path, "wb") as f:
                f.write(iv)
                f.write(ciphertext)
    print("Encryption complete.")

def decrypt_folder(input, output, password, salt_file):
    if not os.path.exists(output):
        os.makedirs(output)

    if not os.path.exists(salt_file):
        print("Error: Salt file does not exist. Please provide a valid salt file.")
        return

    with open(salt_file, 'rb') as f:
        salt = f.read()

    key = bcrypt.kdf(password=password.encode(), salt=salt, desired_key_bytes=16, rounds=100)
    for root, dirs, files in os.walk(input):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, input)
            decrypted_file_path = os.path.join(output, relative_path)
            Path(decrypted_file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "rb") as f:
                iv = f.read(8)
                ciphertext = f.read()

            cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
            plaintext = cipher.decrypt(ciphertext)

            with open(decrypted_file_path, "wb") as f:
                f.write(plaintext)
        print("Decryption complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt and Decrypt Folders using AES in CTR mode")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--encrypt", action='store_true', help="Encrypt folder")
    group.add_argument("-d", "--decrypt", action='store_true', help="Decrypt folder")
    parser.add_argument("-p","--password", help="Password for Encryption/Decryption", type=str, required=True)
    parser.add_argument("-s", "--salt_file", help="Salt file path", type=str)
    parser.add_argument("input", help="Input folder", type=str)
    parser.add_argument("output", help="Output folder path", type=str)
    args = parser.parse_args()

    if args.encrypt:
        encrypt_folder(args.input, args.output, args.password, args.salt_file)

    if args.decrypt:
        decrypt_folder(args.input, args.output, args.password, args.salt_file)