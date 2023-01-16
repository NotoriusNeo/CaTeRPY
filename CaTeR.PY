import argparse
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from pathlib import Path
import bcrypt

def encrypt_folder(folder_to_encrypt, encrypted_folder, password, salt_file):
    if not os.path.exists(folder_to_encrypt):
        print("Error: Folder to encrypt does not exist. Please provide a valid folder path.")
        return
    if not os.path.exists(encrypted_folder):
        os.makedirs(encrypted_folder)
    
    salt = bcrypt.gensalt()
    if salt_file:
        with open(salt_file, 'wb') as f:
            f.write(salt)
    elif salt_file is not None:
        with open(salt_file, 'wb') as f:
            f.write(salt)
    
    key = bcrypt.kdf(password=password.encode(), salt=salt, desired_key_bytes=16, rounds=100)

    for root, dirs, files in os.walk(folder_to_encrypt):
        for file in files:
            iv = get_random_bytes(8) 
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_to_encrypt)
            encrypted_file_path = os.path.join(encrypted_folder, relative_path)
            Path(encrypted_file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "rb") as f:
                plaintext = f.read()

            cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
            ciphertext = cipher.encrypt(plaintext)

            with open(encrypted_file_path, "wb") as f:
                f.write(iv)
                f.write(ciphertext)
    print("Encryption complete.")

def decrypt_folder(folder_to_decrypt, decrypted_folder, password, salt_file):
    if not os.path.exists(decrypted_folder):
        os.makedirs(decrypted_folder)

    if not os.path.exists(salt_file):
        print("Error: Salt file does not exist. Please provide a valid salt file.")
        return

    with open(salt_file, 'rb') as f:
        salt = f.read()

    key = bcrypt.kdf(password=password.encode(), salt=salt, desired_key_bytes=16, rounds=100)
    for root, dirs, files in os.walk(folder_to_decrypt):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_to_decrypt)
            decrypted_file_path = os.path.join(decrypted_folder, relative_path)
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
    parser.add_argument("-e", "--encrypt", action='store_true', help="Encrypt folder")
    parser.add_argument("-d", "--decrypt", action='store_true', help="Decrypt folder")
    parser.add_argument("-p","--password", help="Encryption password", type=str, required=True)
    parser.add_argument("-s", "--salt_file", help="Salt file path", type=str, nargs='?')
    parser.add_argument("folder_to_encrypt", help="Folder to encrypt path", type=str, nargs='?')
    parser.add_argument("encrypted_folder", help="Encrypted folder path", type=str, nargs='?')
    parser.add_argument("folder_to_decrypt", help="Folder to decrypt path", type=str, nargs='?')
    parser.add_argument("decrypted_folder", help="Decrypted folder path", type=str, nargs='?')
    args = parser.parse_args()

    if args.encrypt:
        encrypt_folder(args.folder_to_encrypt, args.encrypted_folder, args.password, args.salt_file)

    if args.decrypt:
        decrypt_folder(args.folder_to_decrypt, args.decrypted_folder, args.password, args.salt_file)
