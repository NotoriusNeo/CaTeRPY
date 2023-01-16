# CaTeR.PY
A python script to recursively encrypt/decrypt folders with AES-CTR, using the pycryptodome and bcrypt libraries.

## Disclaimer / Here be dragons!
!! Things may not work as intended !!

This tool was developed to learn more about encryption/decryption and how it works in Python.
You are the sole responsible and liable to any damage by the usage of this tool.
Please ensure you have a backup of your data before proceeding!

# Usage
This tool was built with python3.11 in mind but may run in lower versions. 

It requires pycryptodome and bcrypt to be installed!

```pip install pycryptodome bcrypt```

### To encrypt
```python3.11 CaTeR.PY -e -p <password> -s <salt file name> <path of folder to encrypt> <output path>```

### To decrypt
```python3.11 CaTeR.PY -d -p <password> -s <salt file name> <path of folder to decrypt> <output path>```

```
usage: CaTeR.PY [-h] [-e | -d] -p PASSWORD [-s SALT_FILE] input output

Encrypt and Decrypt Folders using AES in CTR mode

positional arguments:
  input                 Input folder
  output                Output folder path

options:
  -h, --help            show this help message and exit
  -e, --encrypt         Encrypt folder
  -d, --decrypt         Decrypt folder
  -p PASSWORD, --password PASSWORD
                        Password for Encryption/Decryption
  -s SALT_FILE, --salt_file SALT_FILE
                        Salt file path
```
